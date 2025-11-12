import streamlit as st
import re
from db import add_user, add_tutor
from styles import inject_css

def register_page():
    inject_css("register")
    st.title("📝 Registration Page")

    # CSS for vertical button stacking
    st.markdown("""
    <style>
    .vertical-buttons {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 10px;
        width: 100%;
    }
    .vertical-buttons button {
        width: 50%;
    }
    </style>
    """, unsafe_allow_html=True)

    role_choice = st.selectbox("Register as:", ["Student", "Course Tutor"])

    # ------------------- STUDENT REGISTRATION -------------------
    if role_choice == "Student":
        new_username = st.text_input("Choose a Username")
        type_of_student = st.selectbox("Select type of Student:", ["UG STUDENT", "PGD STUDENT"])
        faculty = st.selectbox("Select Faculty:", [
            'Science', 'Arts', 'Social_&_management_Sciences', 'Administration',
            'Education', 'Health_Sciences', 'Environmental_Sciences'
        ])

        # Department selection based on faculty
        if faculty == 'Science':
            department = st.selectbox("Select Department:", [
                'Biology', 'Computer Sceince', 'Microbiology', 'Biochemistry',
                'Mathematics & Statistics', 'Physics with Electronics',
                'Industrial Chemistry', 'Geology', 'Applied Geophysics'
            ])
        elif faculty == 'Arts':
            department = st.selectbox("Select Department:", [
                'English', 'History & International Studies', 'European Languages', 'Accounting'
            ])
        elif faculty == 'Social_&_management_Sciences':
            department = st.selectbox("Select Department:", [
                'Geography', 'Political Sceince', 'Sociology', 'Economics', 'Demography & Social Statistics'
            ], key='student_social')
        elif faculty == "Health_Sciences":
            department = st.selectbox("Select Department:", [
                'Anatomy', 'Physiology', 'Nursing Sciences', 'Medicine and Surgery'
            ])
        elif faculty == "Environmental_Sciences":
            department = st.selectbox("Select Department:", [
                'Building Technology', 'Architecture', 'Quantity Surveying'
            ])
        elif faculty == "Administration":
            department = st.selectbox("Select Department:", ['Business Administration'])
        elif faculty == "Education":
            department = st.selectbox("Select Department:", [
                'Education Biology', 'Education Computer Sceince', 'Eductaion Chemistry',
                'Education Mathematics', 'Education Physics', 'Education Geography',
                'Eduaction English', 'Education Economics', 'Education Geology'
            ])

        level = st.selectbox("Select Level:", [100, 200, 300, 400, 500, 600])
        email = st.text_input("Enter Email")
        new_password = st.text_input("Choose a Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")

        # Vertical buttons for Student
        st.markdown('<div class="vertical-buttons">', unsafe_allow_html=True)
        student_register_clicked = st.button("Register", key="student_register")
        student_back_clicked = st.button("Back to Login", key="student_back")
        st.markdown('</div>', unsafe_allow_html=True)

        # Handle Student button clicks
        if student_register_clicked:
            if new_password != confirm_password:
                st.error("Passwords do not match!")
            else:
                alphabets = re.findall(r"[A-Za-z]", new_password)
                numbers = re.findall(r"[0-9]", new_password)

                if all([new_username, new_password, department, type_of_student, level, email, faculty]):
                    if alphabets and numbers:
                        if len(new_password) < 6:
                            st.error("Password must be at least 6 characters")
                        elif "@" not in email:
                            st.error("Enter a valid email address")
                        else:
                            add_user(new_username, new_password, department, faculty, level, type_of_student, email, role="User")
                            st.success("🎉 Registration successful! You can now log in.")
                            st.session_state["page"] = "Login"
                            st.rerun()
                    else:
                        st.error("Password must contain both letters and numbers")
                else:
                    st.error("⚠️ Please fill all fields.")

        if student_back_clicked:
            st.session_state["page"] = "Login"
            st.rerun()

    # ------------------- TUTOR REGISTRATION -------------------
    elif role_choice == "Course Tutor":
        tutor_username = st.text_input("Enter Username:")
        faculty = st.selectbox("Select Faculty:", [
            'Science', 'Arts', 'Social_&_management_Sciences', 'Administration',
            'Education', 'Health_Sciences', 'Environmental_Sciences'
        ])

        if faculty == 'Science':
            tutor_department = st.selectbox("Select Department:", [
                'Biology', 'Computer Sceince', 'Microbiology', 'Biochemistry',
                'Mathematics & Statistics', 'Physics with Electronics',
                'Industrial Chemistry', 'Geology', 'Applied Geophysics'
            ])
        elif faculty == 'Arts':
            tutor_department = st.selectbox("Select Department:", [
                'English', 'History & International Studies', 'European Languages', 'Accounting'
            ])
        elif faculty == 'Social_&_management_Sciences':
            tutor_department = st.selectbox("Select Department:", [
                'Geography', 'Political Sceince', 'Sociology', 'Economics', 'Demography & Social Statistics'
            ], key='tutor_social')
        elif faculty == "Health_Sciences":
            tutor_department = st.selectbox("Select Department:", [
                'Anatomy', 'Physiology', 'Nursing Sciences', 'Medicine and Surgery'
            ])
        elif faculty == "Environmental_Sciences":
            tutor_department = st.selectbox("Select Department:", [
                'Building Technology', 'Architecture', 'Quantity Surveying'
            ])
        elif faculty == "Administration":
            tutor_department = st.selectbox("Select Department:", ['Business Administration'])
        elif faculty == "Education":
            tutor_department = st.selectbox("Select Department:", [
                'Education Biology', 'Education Computer Sceince', 'Eductaion Chemistry',
                'Education Mathematics', 'Education Physics', 'Education Geography',
                'Eduaction English', 'Education Economics', 'Education Geology'
            ])

        tutor_id = st.text_input("Enter Tutor ID:")
        tutor_email = st.text_input("Enter Email:")
        tutor_password = st.text_input("Choose a Password", type="password")
        tutor_confirm_password = st.text_input("Confirm Password", type="password")

        # Vertical buttons for Tutor
        st.markdown('<div class="vertical-buttons">', unsafe_allow_html=True)
        tutor_register_clicked = st.button("Register", key="tutor_register")
        tutor_back_clicked = st.button("Back to Login", key="tutor_back")
        st.markdown('</div>', unsafe_allow_html=True)

        # Handle Tutor button clicks
        if tutor_register_clicked:
            if tutor_password != tutor_confirm_password:
                st.error("Passwords do not match!")
            else:
                alphabets = re.findall(r"[A-Za-z]", tutor_password)
                numbers = re.findall(r"[0-9]", tutor_password)

                if all([tutor_username, tutor_password, tutor_department, tutor_id, faculty, tutor_email]):
                    if alphabets and numbers:
                        if len(tutor_password) < 6:
                            st.error("Password must be at least 6 characters")
                        elif "@" not in tutor_email:
                            st.error("Enter a valid email address")
                        else:
                            add_tutor(tutor_username, tutor_password, tutor_department, tutor_id, faculty, tutor_email, role="Tutor")
                            st.success("🎉 Registration successful! You can now log in.")
                            st.session_state["page"] = "Login"
                            st.rerun()
                    else:
                        st.error("Password must contain both letters and numbers")
                else:
                    st.error("⚠️ Please fill all fields.")

        if tutor_back_clicked:
            st.session_state["page"] = "Login"
            st.rerun()
