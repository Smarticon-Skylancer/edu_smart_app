import streamlit as st


def inject_css(role=None):
    """
    Inject polished, responsive CSS for the Streamlit app. This function only
    changes UI styling and preserves existing behavior/API. The `role` value
    only affects the color palette (case-insensitive). Keep signature same
    so existing pages don't need to change.
    """

    # Normalize role lookup and allow session_state to influence theme
    role_norm = (role or "").strip().lower()
    session_role = str(st.session_state.get("role", "")).strip().lower()
    final_role = role_norm or session_role or "general"

    # Default (general/student) color palettes
    primary_color = "#2563eb"  # brand blue (student)
    accent_color = "#7dd3fc"
    hover_color = "#5670c5"
    sidebar_bg = "#0b2447"
    text_color = "#0f172a"
    app_bg_start = "#e6f7fb"
    app_bg_end = "#ffffff"
    card_bg_color = "#ffffff"

    # Tutor / Admin theme (compact, professional)
    if final_role in ("admin", "tutor"):
        primary_color = "#0ea5a4"  # teal/green
        accent_color = "#7fe7d8"
        hover_color = "#08816a"
        sidebar_bg = "#042b2a"
        text_color = "#062023"
        app_bg_start = "#f0fdf9"
        app_bg_end = "#eefaf6"
        card_bg_color = "#fbfffc"  # subtle green tint

    # Student-specific subtle visual variant
    elif final_role == "student":
        primary_color = "#2563eb"
        accent_color = "#7dd3fc"
        hover_color = "#5670c5"
        sidebar_bg = "#0b2447"
        text_color = "#0f172a"
        app_bg_start = "#eaf6ff"
        app_bg_end = "#ffffff"
        card_bg_color = "#ffffff"

    # If this is the login or register page, remove extra top padding so the card sits higher
    auth_css = ""
    if final_role in ("login", "register"):
        auth_css = """
        /* Auth pages: remove top paddings so forms appear higher on the page */
        .stApp { padding-top: 0.25rem !important; }
        .centered-wrapper { padding-top: 0 !important; min-height: calc(100vh - 20px) !important; }
        .centered-card { margin-top: 1vh !important; }
        """

    st.markdown(
        f"""
    <style>
    {auth_css}
    :root {{
            --primary: {primary_color};
            --accent: {accent_color};
            --hover: {hover_color};
            --sidebar-bg: {sidebar_bg};
            --text: {text_color};
            --app-bg-start: {app_bg_start};
            --app-bg-end: {app_bg_end};
            --card-bg: {card_bg_color};
            --muted: #6b7280;
        }}

        /* Reset & base */
        .stApp {{
            background: linear-gradient(180deg, var(--app-bg-start) 0%, var(--app-bg-end) 100%);
            color: var(--text);
            font-family: "Inter", "Segoe UI", Tahoma, sans-serif;
            -webkit-font-smoothing: antialiased;
            padding: 0.75rem 0.75rem; /* smaller global padding so centered cards fit on small screens */
            box-sizing: border-box;
        }}

        /* Headings */
        h1, h2, h3 {{
            color: var(--text);
            font-weight: 700;
            text-align: center;
            margin: 0.35rem 0 0.85rem 0;
            letter-spacing: -0.5px;
        }}

        /* Subtitles and helper text */
        .sub-title, .stMarkdown p {{
            color: var(--muted);
            font-size: 0.95rem;
        }}

        /* Sidebar polished styling */
        section[data-testid="stSidebar"] {{
            background: linear-gradient(180deg, var(--sidebar-bg) 0%, #0b1220 100%);
            color: #f8fafc;
            padding-top: 1rem;
        }}
        section[data-testid="stSidebar"] * {{
            color: #f8fafc !important;
        }}
        /* Add a logo / heading area in sidebar */
        section[data-testid="stSidebar"] .sidebar-logo {{
            display:flex;align-items:center;gap:.75rem;padding:0.6rem 0 1rem 0;margin-bottom:0.4rem;border-bottom:1px solid rgba(255,255,255,0.04)
        }}
        section[data-testid="stSidebar"] .sidebar-logo img{{
            width:40px;height:40px;border-radius:8px;object-fit:cover
        }}

        /* Centered card for forms (login/register) */

        .centered-card {{
            max-width: 560px;
            margin: 2.5vh auto;
            padding: 1.25rem 1.25rem; /* reduced padding to fit on smaller viewports */
            background: var(--card-bg);
            border-radius: 14px;
            box-shadow: 0 8px 26px rgba(16,24,40,0.06);
            border: 1px solid rgba(16,24,40,0.05);
            box-sizing: border-box;
            max-height: calc(100vh - 120px); /* ensure card never exceeds viewport */
            overflow: auto; /* allow internal scroll when content is tall */
        }}

        /* Wrapper to vertically center a card on the page */
        .centered-wrapper {{
            min-height: calc(100vh - 40px);
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 0.5rem 0; /* reduce extra spacing so card centers within visible area */
            box-sizing: border-box;
        }}

        /* Form elements - make inputs more visible and accessible */
        .stTextInput>div>div>input,
        .stNumberInput input,
        .stSelectbox>div>div>select,
        textarea {{
            background: #fff;
            color: var(--text);
            border: 1px solid rgba(15,23,42,0.16); /* stronger border so it is visible */
            border-radius: 10px;
            padding: 10px 12px;
            width: 100%;
            box-shadow: inset 0 1px 0 rgba(255,255,255,0.6);
            outline: none;
            box-sizing: border-box;
        }}
        .stTextInput>div>div>input:focus,
        .stNumberInput input:focus,
        .stSelectbox>div>div>select:focus,
        textarea:focus {{
            border-color: var(--primary);
            box-shadow: 0 8px 20px rgba(2,6,23,0.06);
            outline: none;
        }}

        /* Buttons - larger, full-width on small screens */
        .stButton>button {{
            background: linear-gradient(90deg, var(--primary), var(--hover));
            color: white;
            padding: 10px 16px;
            border-radius: 10px;
            border: none;
            font-weight: 600;
            box-shadow: 0 6px 18px rgba(15,23,42,0.08);
            min-width: 110px;
            transition: transform .06s ease, box-shadow .12s ease;
            display: inline-flex;align-items:center;justify-content:center;gap:.5rem
        }}
        .stButton>button:hover {{
            transform: translateY(-2px);
        }}

        /* Primary action (used by cgpa result or success messages) */
        .cgpa-success {{
            background: var(--primary);
            color: #fff;
            padding: 12px 18px;
            border-radius: 10px;
            text-align: center;
            font-weight: 700;
            font-size: 1.15rem;
            box-shadow: 0 8px 28px rgba(2,6,23,0.06);
        }}

        /* Alert overrides (streamlined) */
        .stAlert {{
            border-radius: 10px;
            padding: 10px 14px;
            margin: .5rem 0;
        }}
        .stAlert--error, .stAlert[data-testid*="stAlert"] .stMarkdown p[style*="color:"] {{
            background: linear-gradient(90deg,#fdecea,#f9d4d6);
            color: #7f1d1d;
        }}
        .stAlert--success {{
            background: linear-gradient(90deg,#ecfdf5,#bbf7d0);
            color: #064e3b;
        }}

        /* Dataframes / tables - subtle card */
        .stDataFrame > div{{
            background: var(--card-bg);
            border-radius: 10px;
            padding: 8px;
            box-shadow: 0 6px 18px rgba(2,6,23,0.03);
            overflow: auto;
        }}
        .stDataFrame table thead th{{
            background: linear-gradient(90deg, rgba(0,0,0,0.03), rgba(0,0,0,0.01));
            color: var(--text);
            font-weight: 700;
        }}

        /* Cards (user, event, message) */
        .user-info-card, .event-card, .message-card {{
            background: var(--card-bg);
            border-radius: 14px;
            padding: 18px;
            box-shadow: 0 8px 26px rgba(2,6,23,0.04);
            margin: 0.85rem 0;
            overflow: visible; /* allow content to show fully */
            word-break: break-word;
            white-space: normal;
            line-height: 1.45;
        }}
        .user-info-card h2, .event-card h2 {{
            color: var(--text);
            font-size: 1.25rem; /* slightly smaller for compact, professional look */
            margin-bottom: .45rem;
            text-align: center;
            line-height: 1.2;
            word-break: normal;
        }}
        .user-info-card p, .event-card p {{
            color: var(--muted);
            font-size: 0.98rem;
            margin: .35rem 0;
            white-space: normal;
        }}

        /* Ensure Streamlit info/warning boxes wrap text cleanly */
        .stAlert, .stInfo, .stWarning, .stSuccess, .stError, .stMarkdown p {{
            white-space: normal !important;
            word-break: break-word !important;
            line-height: 1.4 !important;
        }}

        /* Message card variations */
        .message-card{{
            border-left: 4px solid var(--accent);
            width:100%;
            text-align: left;
            font-family: Tahoma, sans-serif;
        }}

        /* Labels */
        .labels{{
            font-size: 1rem;
            font-family: Tahoma, sans-serif;
            color: var(--muted);
        }}

        /* Responsive behavior */
        @media (max-width: 640px) {{
            .centered-card {{
                margin: 3vh 1rem;
                padding: 1rem;
            }}
            .stButton>button {{
                width: 100%;
            }}
            .message-card{{
                width:100%!important;
                margin-left:0!important;
            }}
        }}

        /* Small utilities */
        .muted {{ color: var(--muted); font-size: .95rem }}
        .mono {{ font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, monospace }}

        /* Chat styles */
        .chat-container {{
            display: flex;
            flex-direction: column;
            gap: .6rem;
            padding: .5rem;
        }}
        .msg-row {{
            display:flex;
            align-items:flex-end;
            gap: .6rem;
        }}
        .msg-left {{ justify-content: flex-start; }}
        .msg-right {{ justify-content: flex-end; }}
        .msg-bubble {{
            max-width: 78%;
            padding: .6rem .8rem;
            border-radius: 12px;
            font-size: .95rem;
            line-height: 1.3;
            box-shadow: 0 6px 14px rgba(2,6,23,0.06);
        }}
        .msg-user {{
            background: linear-gradient(90deg, var(--primary), var(--accent));
            color: white;
            border-bottom-right-radius: 4px;
        }}
        .msg-other {{
            background: #f1f5f9;
            color: var(--text);
            border-bottom-left-radius: 4px;
        }}
        .msg-meta {{ font-size: 11px; color: var(--muted); margin-top: 4px; }}
        .msg-avatar {{ width:36px;height:36px;border-radius:50%;display:inline-flex;align-items:center;justify-content:center;font-weight:700;color:white }}

        /* Hide Streamlit default chrome and sharing links for cleaner, app-like UI
           ONLY on larger screens — keep Streamlit menu/footer visible on small/mobile
           so users can access navigation and sharing features. */
        @media (min-width: 800px) {{
            #MainMenu {{ visibility: hidden; }}
            header {{ visibility: hidden; }}
            footer {{ visibility: hidden; }}
            /* Also hide the Streamlit branding that can appear in some embeds */
            .css-1lsmgbg {{ display: none !important; }}
        }}

        /* On small screens, make sure default chrome is visible so the mobile user
           can access the hamburger menu and page navigation */
        @media (max-width: 799px) {{
            #MainMenu {{ visibility: visible !important; }}
            header {{ visibility: visible !important; }}
            footer {{ visibility: visible !important; }}
            .css-1lsmgbg {{ display: block !important; }}
        }}

        </style>
        """,
        unsafe_allow_html=True,
    )
