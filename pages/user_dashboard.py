import streamlit as st
from styles import inject_css
from pages.gpa_calculator import cgpa_calculator_page
from pages.timetable import time_table_generator

def user_dashboard():
    user = st.session_state.get("user", "Unknown")
    department = st.session_state.get("department", "Unknown")
    email = st.session_state.get("email", "Unknown")
    level = st.session_state.get("level", "Unknown")
    type_of_student = st.session_state.get("type_of_student", "Unknown")

    user_option = st.sidebar.radio("Navigation", ["Dashboard", "Timetable Generator", "GPA Calculator", "Assignments", "Logout"])

    if user_option == "Dashboard":
        inject_css("general")
        st.markdown(f"""
        <div class="user-info-card">
            <h2>🎓 Welcome Back {user}</h2>
            <p><strong>Department:</strong> {department}</p><hr>
            <p><strong>Email:</strong> {email}</p><hr>
            <p><strong>Level:</strong> {level}</p><hr>
            <p><strong>Type of Student:</strong> {type_of_student}</p>
        </div>
        """, unsafe_allow_html=True)

    elif user_option == "Timetable Generator":
        time_table_generator()
    elif user_option == "GPA Calculator":
        cgpa_calculator_page(user)
    elif user_option == "Assignments":
        inject_css("general")
        st.subheader("📌 Feature coming soon...")
    elif user_option == "Logout":
        st.session_state.clear()
        st.rerun()
