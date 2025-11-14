import streamlit as st
from db import login_user, login_tutor
from styles import inject_css
from app_pages.home import home_page
import time as t     
     

def login_page():
    inject_css("login")

    # Center the login card vertically and horizontally
    st.markdown('<div class="centered-card">', unsafe_allow_html=True)
    st.title("🔐 Login to EduSmart System")

    role = st.selectbox("Select Role:", ["Student", "Course Tutor"])
    username_input = st.text_input("Username")
    password_input = st.text_input("Password", type="password")

    login_clicked = st.button("🔑 Login", use_container_width=True)
        
        
        
    if login_clicked:
        if not username_input or not password_input:
            st.warning("⚠️ Please enter both username and password.")
        else:
            if role == "Student":
                firstname, surname, username, student_id,role, gender, faculty, department, level,email, type_of_student= login_user(username_input, password_input)
                if username:
                    st.session_state.update({
                        "firstname": firstname,
                        "surname": surname, 
                        "user": username,
                        "student_id": student_id,
                        "role": role,
                        "gender": gender,
                        "faculty": faculty,
                        "department": department,
                        "level": level,
                        "email": email,
                        "type_of_student": type_of_student,
                        "page": "Student"
                    })
                    st.success("✅ Login successful!")
                    st.rerun()
                else:
                    st.error("❌ Invalid username or password")
            # --- login block ---
            elif role == "Course Tutor":
                firstname, surname, gender, tutor_id, tutor_username, tutor_department, faculty, tutor_email, role = login_tutor(username_input, password_input)
                
                if tutor_username:  # Login successful
                    st.session_state.update({
                        "firstname": firstname,
                        "surname": surname,
                        "gender": gender,
                        "tutor_ID": tutor_id,
                        "user": tutor_username,
                        "department": tutor_department,
                        "faculty": faculty,
                        "email": tutor_email,
                        "role": role,
                        "page": "Tutor"
                    })
                    st.success("✅ Login successful !!!")
                    t.sleep(2)
                    st.rerun()
                else:
                    st.error("❌ Login failed. Check username and password.")

    # close the centered wrapper
    st.markdown('</div></div>', unsafe_allow_html=True)

