import streamlit as st
from db import login_user, login_admin
from styles import inject_css

def login_page():
    inject_css("login")
    st.markdown('<div class="centered-card">', unsafe_allow_html=True)
    st.title("🔐 Login to EduSmart System")

    role = st.selectbox("Select Role:", ["Student", "Admin"])
    username_input = st.text_input("Username")
    password_input = st.text_input("Password", type="password")

    if st.button("Login"):
        if not username_input or not password_input:
            st.warning("⚠️ Please enter both username and password.")
        else:
            if role == "Admin":
                user, role_returned = login_admin(username_input, password_input)
                dept, lvl, type_stu, email = None, None, None, None
            else:
                user, role_returned, dept, lvl, type_stu, email = login_user(username_input, password_input)

            if user:
                st.session_state.update({
                    "user": user,
                    "role": role_returned,
                    "department": dept,
                    "level": lvl,
                    "type_of_student": type_stu,
                    "email": email,
                    "page": role_returned
                })
                st.success("✅ Login successful!")
                st.rerun()
            else:
                st.error("❌ Invalid username or password")

    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("Don't have an account? Register"):
        st.session_state["page"] = "Register"
        st.rerun()
