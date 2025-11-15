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

    # Minimal sidebar: only render the navigation radio so the sidebar does not collapse into
    # a top selectbox on mobile with other widgets. This keeps the sidebar focused on navigation.
    if nav_options is None:
        nav_options = []

    st.sidebar.markdown("<div style='padding:0.5rem 0;'></div>", unsafe_allow_html=True)
    selected = st.sidebar.radio("", nav_options, index=0 if nav_options else None, key=f"{key_prefix}_radio")
    return selected
