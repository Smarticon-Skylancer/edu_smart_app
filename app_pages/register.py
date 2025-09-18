import streamlit as st
import re
from db import add_user
from styles import inject_css

def register_page():
    inject_css("register")
    st.markdown("<div class='register-title'>📝 Register</div>", unsafe_allow_html=True)

    new_username = st.text_input("Choose a Username")
    department = st.text_input("Enter Department")
    type_of_student = st.selectbox("Select type of Student:", ["UG STUDENT", "PGD STUDENT"])
    level = st.selectbox("Select Level:", [100, 200, 300, 400, 500, 600])
    email = st.text_input("Enter Email")

    new_password = st.text_input("Choose a Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Register"):
        if new_password != confirm_password:
            st.error("Passwords do not match!")
        else:
            alphabets = re.findall(r"[A-Za-z]", new_password)
            numbers = re.findall(r"[0-9]", new_password)

            if all([new_username, new_password, department, type_of_student, level, email]):
                if alphabets and numbers:
                    if len(new_password) < 6:
                        st.error("Password must be at least 6 characters")
                    elif "@" not in email:
                        st.error("Enter a valid email address")
                    else:
                        add_user(new_username, new_password, department, level, type_of_student, email, role="User")
                        st.success("🎉 Registration successful! You can now log in.")
                        st.session_state["page"] = "Login"
                        st.rerun()
                else:
                    st.error("Password must contain both letters and numbers")
            else:
                st.error("⚠️ Please fill all fields.")

    if st.button("Back to Login"):
        st.session_state["page"] = "Login"
        st.rerun()
