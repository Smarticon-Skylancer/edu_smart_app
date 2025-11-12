import streamlit as st
from db import login_user, login_tutor
from styles import inject_css
from app_pages.home import home_page        

def login_page():
    inject_css("login")

    st.markdown('<div class="centered-card">', unsafe_allow_html=True)
    st.title("🔐 Login to EduSmart System")

    role = st.selectbox("Select Role:", ["Student", "Course Tutor"])
    username_input = st.text_input("Username")
    password_input = st.text_input("Password", type="password")

    col1, col2 = st.columns([1, 1], gap='small')
    with col1:
        login_clicked = st.button("🔑 Login", use_container_width=True)
        
    with col2:
        back_clicked = st.button("📝 Register", use_container_width=True)
        
    if login_clicked:
        if not username_input or not password_input:
            st.warning("⚠️ Please enter both username and password.")
        else:
            if role == "Student":
                user, role_returned, dept, lvl, type_stu, fac, email = login_user(username_input, password_input)
                if user:
                    st.session_state.update({
                        "user": user,
                        "role": role_returned,
                        "department": dept,
                        "level": lvl,
                        "type_of_student": type_stu,
                        "email": email,
                        "faculty": fac,
                        "page": "Student"
                    })
                    st.success("✅ Login successful!")
                    st.rerun()
                else:
                    st.error("❌ Invalid username or password")
            elif role == "Course Tutor":
                user, role_returned, tutor_dept, tutor_faculty, tutor_email, tutor_ID = login_tutor(username_input, password_input)
                if user:
                    st.session_state.update({
                        "user": user,
                        "role": role_returned,
                        "department": tutor_dept,
                        "faculty": tutor_faculty,
                        "email": tutor_email,
                        "tutor_ID": tutor_ID,
                        "page": "admin"
                    })
                    st.success("✅ Login successful!")
                    st.rerun()
                else:
                    st.error("❌ Invalid username or password")

    if back_clicked:
        st.session_state["page"] = "Register"
        st.rerun()

