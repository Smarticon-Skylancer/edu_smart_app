import streamlit as st
from db import init_db
from db import init_admin_db
from app_pages.login import login_page
from app_pages.register import register_page
from app_pages.admin_dashboard import admin_dashboard
from app_pages.user_dashboard import user_dashboard
from app_pages.home import home_page


init_db()
init_admin_db()

if "page" not in st.session_state:
    home_page()
elif st.session_state["page"] == "Login":
    login_page()
elif st.session_state["page"] == "Register":
    register_page()
elif st.session_state["page"] == "admin":
    admin_dashboard()
elif st.session_state["page"] == "Student":
    user_dashboard()
