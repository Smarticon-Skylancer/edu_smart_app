import streamlit as st
import os
from pathlib import Path
from io import BytesIO

# Optional Pillow import for image handling
try:
    from PIL import Image
    PIL_AVAILABLE = True
except Exception:
    PIL_AVAILABLE = False


def render_sidebar(display_name=None, role=None, faculty=None, department=None, avatar_svg=None, nav_options=None, key_prefix="nav"):
    """
    Render a compact, branded sidebar with profile card, navigation, and logout.
    - display_name: str shown in the profile area
    - role: Student/Tutor/Admin label
    - faculty/department: optional small metadata lines
    - avatar_svg: optional inline SVG string for avatar; if None we render initials
    - nav_options: list of strings for navigation items
    Returns the selected navigation option (string)
    """

    if nav_options is None:
        nav_options = []

    # Brand area (logo already added from app.py but keep spacing)
    st.sidebar.markdown("<div style='padding:0.35rem 0 0.6rem 0;'></div>", unsafe_allow_html=True)

    # Profile card with optional avatar upload
    with st.sidebar.container():
        st.markdown("<div style='display:flex; align-items:center; gap:0.6rem;'>", unsafe_allow_html=True)

        # Determine username (use display_name fallback)
        username = display_name or st.session_state.get("user", "user")
        safe_name = "".join([c for c in username if c.isalnum() or c in (' ', '_', '-')]).strip().replace(' ', '_').lower()

        # Ensure profiles dir exists
        profiles_dir = Path(os.getcwd()) / "user_profiles"
        try:
            profiles_dir.mkdir(parents=True, exist_ok=True)
        except Exception:
            profiles_dir = Path("user_profiles")

        # Expected avatar path
        avatar_path = profiles_dir / f"{safe_name}.png"

        # If an avatar file exists on disk, show it. Otherwise render initials and allow upload.
        if avatar_path.exists():
            try:
                st.sidebar.image(str(avatar_path), width=56)
            except Exception:
                # fallback to initials rendering if image invalid
                avatar_svg = None

        if not avatar_path.exists():
            if avatar_svg:
                st.sidebar.markdown(avatar_svg, unsafe_allow_html=True)
            else:
                # render initials circle
                name = display_name or "User"
                initials = "".join([p[0] for p in name.split()][:2]).upper()
                st.sidebar.markdown(
                    f"<div style='width:44px;height:44px;border-radius:50%;background:linear-gradient(90deg,var(--primary),var(--accent));display:inline-flex;align-items:center;justify-content:center;color:white;font-weight:700'>{initials}</div>",
                    unsafe_allow_html=True,
                )

            # File uploader to set profile picture
            uploaded = st.sidebar.file_uploader("Upload profile image", type=["png", "jpg", "jpeg"], key=f"{key_prefix}_avatar_uploader")
            if uploaded is not None:
                # Validation: max size 2MB
                try:
                    uploaded_bytes = uploaded.getvalue()
                    max_bytes = 2 * 1024 * 1024  # 2MB
                    if len(uploaded_bytes) > max_bytes:
                        st.sidebar.error("Image too large — please upload <= 2 MB")
                    else:
                        # Process image: if Pillow available, resize and save as PNG
                        img_path = profiles_dir / f"{safe_name}.png"
                        if PIL_AVAILABLE:
                            try:
                                img = Image.open(BytesIO(uploaded_bytes))
                                # Convert to RGBA to preserve transparency if any, then to RGB
                                img = img.convert("RGBA")
                                # Resize to max 512px keeping aspect ratio, then fit to 256x256 square
                                img.thumbnail((512, 512))
                                # Create square background
                                out = Image.new("RGBA", (256, 256), (255, 255, 255, 0))
                                # center the thumbnail
                                x = (256 - img.width) // 2
                                y = (256 - img.height) // 2
                                out.paste(img, (x, y), img)
                                out = out.convert("RGB")
                                out.save(img_path, format="PNG")
                            except Exception as e:
                                st.sidebar.error(f"Image processing failed: {e}")
                                # fallback: write raw bytes
                                with open(img_path, "wb") as f:
                                    f.write(uploaded_bytes)
                        else:
                            # Pillow not available — save raw bytes
                            with open(img_path, "wb") as f:
                                f.write(uploaded_bytes)

                        # store in session so other pages can use immediately
                        st.session_state.setdefault("avatar_path", str(img_path))
                        # show preview
                        st.sidebar.image(str(img_path), width=56)
                except Exception as e:
                    st.sidebar.error(f"Unable to save avatar image: {e}")
        
        # If an avatar was not just uploaded but exists in session_state, show it
        if not avatar_path.exists() and st.session_state.get("avatar_path") and Path(st.session_state.get("avatar_path")).exists():
            try:
                st.sidebar.image(st.session_state.get("avatar_path"), width=56)
            except Exception:
                pass

        # Remove avatar button
        if st.sidebar.button("Remove avatar", key=f"{key_prefix}_remove_avatar"):
            try:
                # remove on-disk file if exists
                p = Path(st.session_state.get("avatar_path", ""))
                if p.exists():
                    p.unlink()
                # clear session state
                if "avatar_path" in st.session_state:
                    del st.session_state["avatar_path"]
                st.sidebar.success("Avatar removed")
                try:
                    st.experimental_rerun()
                except Exception:
                    st.stop()
            except Exception as e:
                st.sidebar.error(f"Could not remove avatar: {e}")

        st.sidebar.markdown(
            f"<div style='display:inline-block; vertical-align:middle;'>"
            f"<div style='font-weight:700; color:var(--text);'>{display_name or 'EduSmart User'}</div>"
            f"<div style='font-size:12px; color:var(--muted);'>{role or ''} "
            f"{('| ' + department) if department else ''} {('| ' + faculty) if faculty else ''}</div>"
            f"</div>",
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

    st.sidebar.markdown("---")

    # Navigation
    # Use a radio in the sidebar for desktop and a selectbox for mobile users.
    # We'll track which control the user interacted with via on_change callbacks
    def _sidebar_nav_changed():
        st.session_state[f"{key_prefix}_nav_source"] = "sidebar"

    def _mobile_nav_changed():
        st.session_state[f"{key_prefix}_nav_source"] = "mobile"

    selected = st.sidebar.radio("", nav_options, index=0, key=f"{key_prefix}_radio", on_change=_sidebar_nav_changed)

    st.sidebar.markdown("---")

    # Logout + help area
    if st.sidebar.button("🔒 Logout", key=f"{key_prefix}_logout"):
        # clear session and rerun (safe fallback if experimental_rerun is unavailable)
        st.session_state.clear()
        # place user on Login page explicitly
        st.session_state["page"] = "Login"
        # Try experimental rerun if available; otherwise stop current run so Streamlit processes the next rerun.
        try:
            rerun = getattr(st, "experimental_rerun")
            rerun()
        except Exception:
            # st.stop will end current script execution; Streamlit will perform a rerun after the widget event.
            st.stop()

    st.sidebar.markdown("<div style='font-size:11px;color:var(--muted);padding-top:8px;'>EduSmart • v1.0</div>", unsafe_allow_html=True)

    # Mobile-friendly top navigation (appears in main area) — users on phones can use this
    try:
        mobile_choice = st.selectbox("", nav_options, index=0, key=f"{key_prefix}_mobile_nav", on_change=_mobile_nav_changed)
    except Exception:
        # In case selectbox fails to render in some contexts, fall back to sidebar choice
        mobile_choice = None

    # Decide which nav to return based on the last widget the user interacted with
    nav_source = st.session_state.get(f"{key_prefix}_nav_source", "sidebar")
    if nav_source == "mobile" and mobile_choice:
        return mobile_choice
    return selected
