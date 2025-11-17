
import streamlit as st
from db import init_db
from db import init_admin_db
from app_pages.login import login_page
from app_pages.register import register_page
from app_pages.admin_dashboard import admin_dashboard
from app_pages.user_dashboard import user_dashboard
from app_pages.home import home_page
from styles import inject_css 
from app_pages.guestMode import guest_page
from portfolio import about_us,contact_dev
from app_pages.timetable import time_table_generator
from app_pages.gpa_calculator import cgpa_calculator_page


init_db()
init_admin_db()

# Inject global styles and a small sidebar logo placeholder for branding
inject_css()
# Simple inline SVG logo as a placeholder (no external assets required)
st.sidebar.markdown(
        '''
        <div class="sidebar-logo">
            <svg xmlns="http://www.w3.org/2000/svg" width="70" height="70" viewBox="0 0 100 100" role="img" aria-label="EduSmart logo">
                <defs>
                    <linearGradient id="g" x1="0" x2="1">
                        <stop offset="0" stop-color="#2563eb" />
                        <stop offset="1" stop-color="#7dd3fc" />
                    </linearGradient>
                </defs>
                <rect rx="18" width="100" height="100" fill="url(#g)" />
                <text x="50" y="58" font-size="48" text-anchor="middle" fill="white" font-family="Inter, Arial">ES</text>
            </svg>
            <div style="display:inline-block; vertical-align:middle;">
                <div style="font-weight:700; color:#fff;">EduSmart</div>
                <div style="font-size:11px; color:rgba(255,255,255,0.8);">v2.0</div>
            </div>
        </div>
        '''
        , unsafe_allow_html=True)
st.sidebar.button("🏠 Home", key=f"home", on_click=lambda: st.session_state.update({"page" : "Home"}))
st.sidebar.button("👨‍💻 Developer's Portfolio", key="dev_port", on_click=lambda : st.session_state.update({"page" : "Developer"}))
    
st.sidebar.button("☎️ Contact Developer", key="contact_dev", on_click=lambda : st.session_state.update({"page" : "Contact"}))
    

# Main page routing logic
if "page" not in st.session_state:
    home_page()
elif st.session_state["page"] == "Home":
    home_page()
elif st.session_state['page'] == "Guest":
    guest_page()
elif st.session_state['page'] == "Developer":
    about_us()
elif st.session_state['page'] == 'Contact':
    contact_dev()
elif st.session_state["page"] == "Login":
    login_page()
elif st.session_state["page"] == "Register":
    register_page()
elif st.session_state["page"] == "Tutor":
    admin_dashboard()
elif st.session_state["page"] == "Student":
    user_dashboard()
elif st.session_state["page"] == "Timetable":
    
    time_table_generator()
elif st.session_state["page"] == "GPA Calculator":
    
    cgpa_calculator_page(user = False)
else:
    st.session_state['page'] = "Home"