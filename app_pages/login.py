import streamlit as st
from db import login_user, login_tutor
from styles import inject_css
from app_pages.home import home_page        

def login_page():
    inject_css("login")

    # CSS for vertical buttons
    st.markdown("""
    <style>
    .vertical-buttons {
        display: flex;
        flex-direction: column;  /* stack vertically */
        align-items: center;     /* center horizontally */
        gap: 10px;               /* spacing between buttons */
        width: 100%;
    }
    .vertical-buttons button {
        width: 50%;              /* width of buttons */
    }
    .centered-card {
        max-width: 500px;
        margin: auto;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="centered-card">', unsafe_allow_html=True)
    st.title("🔐 Login to EduSmart System")

    role = st.selectbox("Select Role:", ["Student", "Course Tutor"])
    username_input = st.text_input("Username")
    password_input = st.text_input("Password", type="password")

    # Vertical buttons container
    st.markdown('<div class="vertical-buttons">', unsafe_allow_html=True)
    login_clicked = st.button("Login", key="login_btn")
    st.info("Don't have an account ?")
    back_clicked = st.button("Register for free", key="register_btn")
    home_clicked = st.button("🏠 Back to Home", key="home_btn")
    st.markdown('</div>', unsafe_allow_html=True)

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
    if home_clicked:
        st.session_state.clear()
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
