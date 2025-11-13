import streamlit as st
import re
from db import add_user, add_tutor
from styles import inject_css


def register_page():
    inject_css("register")
    st.title("📝 Registration Page")

    role_choice = st.selectbox("Register as:", ["Student", "Course Tutor"])

    # Faculties and Departments
    faculties = {
        "Science": [
            "Biology", "Computer Science", "Microbiology", "Biochemistry",
            "Mathematics & Statistics", "Physics with Electronics",
            "Industrial Chemistry", "Geology", "Applied Geophysics"
        ],
        "Arts": ["English", "History & International Studies", "European Languages", "Accounting"],
        "Social_&_Management_Sciences": [
            "Geography", "Political Science", "Sociology", "Economics", "Demography & Social Statistics"
        ],
        "Health_Sciences": ["Anatomy", "Physiology", "Nursing Sciences", "Medicine and Surgery"],
        "Environmental_Sciences": ["Building Technology", "Architecture", "Quantity Surveying"],
        "Administration": ["Business Administration"],
        "Education": [
            "Education Biology", "Education Computer Science", "Education Chemistry",
            "Education Mathematics", "Education Physics", "Education Geography",
            "Education English", "Education Economics", "Education Geology"
        ]
    }

    # =====================================
    # STUDENT REGISTRATION SECTION
    # =====================================
    if role_choice == "Student":
        st.subheader("👨‍🎓 Student Registration")
        firstname = st.text_input("Enter First Name")
        surname = st.text_input("Enter Surname")
        gender = st.selectbox("Select Gender:", ["Male", " Female", "Other"])
        student_id = st.text_input("Student ID")
        username = st.text_input("Choose a Username")
        type_of_student = st.selectbox("Select Type of Student:", ["UG STUDENT", "PGD STUDENT"])
        faculty = st.selectbox("Select Faculty:", list(faculties.keys()))
        department = st.selectbox("Select Department:", faculties[faculty])
        level = st.selectbox("Select Level:", [100, 200, 300, 400, 500, 600])
        email = st.text_input("Enter Email")
        password = st.text_input("Choose a Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        

        col1, col2 = st.columns(2)
        with col1:
            register_btn = st.button("Register", use_container_width=True)
        with col2:
            back_btn = st.button("Back to Login", use_container_width=True)

        if register_btn:
            # Basic validation
            if not all([username, password, confirm_password, email, faculty, department, level, type_of_student]):
                st.error("⚠️ Please fill in all fields.")
            elif password != confirm_password:
                st.error("❌ Passwords do not match!")
            elif len(password) < 6:
                st.error("🔒 Password must be at least 6 characters long.")
            elif not re.search(r"[A-Za-z]", password) or not re.search(r"[0-9]", password):
                st.error("🔤 Password must contain both letters and numbers.")
            elif "@" not in email or "." not in email:
                st.error("📧 Enter a valid email address.")
            elif len(student_id) != 10:
                st.error("Student ID must be exactly 10 characters long.")
            else:
                # Call db.py add_user
                add_user(firstname, surname, username, student_id, gender, password, faculty, department, level, type_of_student, email, role="Student")
                st.session_state["page"] = "Login"
                st.rerun()

        if back_btn:
            st.session_state["page"] = "Login"
            st.rerun()

    # =====================================
    # TUTOR REGISTRATION SECTION
    # =====================================
    elif role_choice == "Course Tutor":
        st.subheader("👩‍🏫 Tutor Registration")
        firstname = st.text_input("Enter First Name")
        surname = st.text_input("Enter Surname")  
        gender = st.selectbox("Select Gender:", ["Male", " Female", "Other"])
        tutor_username = st.text_input("Tutor Username")
        tutor_id = st.text_input("Tutor ID")
        faculty = st.selectbox("Select Faculty:", list(faculties.keys()))
        tutor_department = st.selectbox("Select Department:", faculties[faculty])
        tutor_email = st.text_input("Tutor Email")
        tutor_password = st.text_input("Choose a Password", type="password")
        tutor_confirm_password = st.text_input("Confirm Password", type="password")

        col1, col2 = st.columns(2)
        with col1:
            register_btn = st.button("Register", use_container_width=True)
        with col2:
            back_btn = st.button("Back to Login", use_container_width=True)

        if register_btn:
            if not all([tutor_username, tutor_password, tutor_confirm_password, tutor_email, tutor_id, faculty, tutor_department]):
                st.error("⚠️ Please fill in all fields.")
            elif tutor_password != tutor_confirm_password:
                st.error("❌ Passwords do not match!")
            elif len(tutor_password) < 6:
                st.error("🔒 Password must be at least 6 characters long.")
            elif not re.search(r"[A-Za-z]", tutor_password) or not re.search(r"[0-9]", tutor_password):
                st.error("🔤 Password must contain both letters and numbers.")
            elif "@" not in tutor_email or "." not in tutor_email:
                st.error("📧 Enter a valid email address.")
            elif len(tutor_id) != 8:
                st.error("Tutor ID must be exactly 8 characters long.")
            else:
                # Call db.py add_tutor
                add_tutor(firstname, surname, gender, tutor_username, tutor_password, tutor_department, faculty, tutor_id, tutor_email, role="Tutor")
                st.session_state["page"] = "Login"
                st.rerun()

        if back_btn:
            st.session_state["page"] = "Login"
            st.rerun()
