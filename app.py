import streamlit as st
import pandas as pd
import re

from db import init_db, add_user, login_user, login_admin, fetch_all_users, remove_user
from courses import load_courses, save_courses
from styles import inject_css

# -------------------------------
# User Dashboard (CGPA Calculator)
# -------------------------------
def cgpa_calculator_page():
    inject_css("general")
    
    df_courses = load_courses()
    st.header("🎓 CGPA Calculator")
    st.markdown("<div class='sub-title'>Select your level, enter grades, and calculate your GPA easily.</div>", unsafe_allow_html=True)
    st.write("---")

    if df_courses.empty:
        st.warning("⚠️ No courses available. Please contact the Admin.")
        return

    level = st.selectbox("📌 Select Your Level:", df_courses["Level"].unique())
    level_courses = df_courses[df_courses["Level"] == level]["Course"].unique().tolist()

    num_courses = st.number_input(f"Enter number of courses (Max: {len(level_courses)}):",
                                  min_value=1, max_value=len(level_courses), step=1)

    st.write("### 📚 Enter Your Course Details")
    course_inputs = []
    grade_points = {"A": 5, "B": 4, "C": 3, "D": 2, "E": 1, "F": 0}

    for i in range(num_courses):
        st.write(f"#### Course {i+1}")
        course = st.selectbox(f"Select Course {i+1}", level_courses, key=f"course_{i}")
        credit_unit = st.number_input(f"Enter Credit Units for {course}", min_value=1, max_value=6, step=1, key=f"credit_{i}")
        grade = st.selectbox(f"Enter Grade for {course}", options=list(grade_points.keys()), key=f"grade_{i}")
        course_inputs.append({"Course": course, "CreditUnit": credit_unit, "Grade": grade})

    if st.button("🎯 Calculate GPA", key='Calculate_cgpa'):
        total_units = sum([c["CreditUnit"] for c in course_inputs])
        total_points = sum([c["CreditUnit"] * grade_points[c["Grade"]] for c in course_inputs])
        gpa = total_points / total_units if total_units > 0 else 0

        st.write("### 📊 Breakdown of Results")
        st.dataframe(pd.DataFrame(course_inputs))
        st.success(f"✅ Your GPA is: **{gpa:.2f}**")
        if gpa >= 4.5:
            st.write("Class of Degree : First Class")
        elif gpa >= 3.5:
            st.write("Class of Degree : Second Class Upper")
        elif gpa >= 2.5:
            st.write("Class of Degree : Second Class Lower")
        elif gpa >= 1.5:
            st.write("Class of Degree : Third Class")
        else:
            st.error("Class of Degree : Please check with the school.")

# -------------------------------
# Admin Dashboard
# -------------------------------
def admin_dashboard():
    inject_css("admin")
    st.markdown("<div class='admin-title'>📊 Admin Dashboard</div>", unsafe_allow_html=True)
    st.header('Welcome Smart')

    df_courses = load_courses()
    admin_option = st.sidebar.radio("Navigation", ["Dashboard", "Add a Course", "Remove a Course", "Remove a User", "Logout"])

    if admin_option == "Dashboard":
        st.subheader("👨‍🏫 Manage Courses")
        st.dataframe(df_courses)

        st.write("### 👥 Registered Users")
        users = fetch_all_users()
        if users:
            df = pd.DataFrame(users, columns=["Username", "Role"])
            st.dataframe(
            df.style.set_properties(
                **{
            'background-color': "green",  # light blue background
            'color': 'white',                # text color
        }))
            
        else:
            st.info("No registered users found.")

    elif admin_option == "Add a Course":
        st.subheader("➕ Add a Course")
        new_level = st.text_input("Enter Level")
        new_course = st.text_input("Course Name")
        if st.button("Add Course", key='Add_course'):
            if new_level and new_course:
                if new_course in df_courses['Course'].values:
                    st.error('⚠️ Course already exists!')
                else:
                    df_courses = pd.concat([df_courses, pd.DataFrame([{"Level": new_level, "Course": new_course}])], ignore_index=True)
                    save_courses(df_courses)
                    st.success(f"Course {new_course} added successfully!")
            else:
                st.error("⚠️ Please fill all fields.")

    elif admin_option == "Remove a Course":
        st.subheader("➖ Remove a Course")
        if not df_courses.empty:
            course_to_remove = st.selectbox("Select course to remove", df_courses["Course"].unique())
            if st.button("Remove Course", key='Remove_course'):
                df_courses = df_courses[df_courses["Course"] != course_to_remove]
                save_courses(df_courses)
                st.success(f"Course {course_to_remove} removed successfully!")
        else:
            st.info("No courses available to remove.")

    elif admin_option == "Remove a User":
        st.subheader("➖ Remove a User")
        users = fetch_all_users()
        df_users = pd.DataFrame(users, columns=["Username", "Role"])
        if not df_users.empty:
            user_to_remove = st.selectbox("Select User to remove", df_users["Username"].unique())
            if st.button("Remove User", key='Remove_user'):
                remove_user(user_to_remove)
                st.success(f"User {user_to_remove} removed successfully!")
        else:
            st.info("No users available to remove.")

    elif admin_option == "Logout":
        st.session_state.clear()
        st.rerun()

# -------------------------------
# Main App
# -------------------------------
st.set_page_config(page_title="CGPA Calculator App", layout="wide")
init_db()

if "page" not in st.session_state:
    st.session_state["page"] = "Login"

# -------------------------------
# Login Page
# -------------------------------
if st.session_state["page"] == "Login":
    inject_css("login")
    st.markdown('<div class="centered-card">', unsafe_allow_html=True)
    st.title("🔐 Login to Smart GPA Calculator")

    role = st.selectbox("Select Role:", ["Student", "Admin"])
    username_input = st.text_input("Username", key="login_user")
    password_input = st.text_input("Password", type="password", key="login_password")

    if st.button("Login", key='login_button'):
        if role == "Admin":
            user, role_returned = login_admin(username_input, password_input)
        else:
            user, role_returned = login_user(username_input, password_input)

        if user:
            st.session_state['user'] = user
            st.session_state['role'] = role_returned
            st.session_state['page'] = role_returned
            st.rerun()
        else:
            st.error("❌ Invalid username or password")

    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("Don't have an account? Register as User", key='reg_button'):
        st.session_state["page"] = "Register"
        st.rerun()

# -------------------------------
# Registration Page
# -------------------------------
elif st.session_state["page"] == "Register":
    inject_css("register")
    st.markdown("<div class='register-title'>📝 Register as User</div>", unsafe_allow_html=True)

    new_username = st.text_input("Choose a Username", key='reg_username')
    new_password = st.text_input("Choose a Password", type="password", key='reg_password')
    confirm_password = st.text_input("Confirm Password", type="password", key='confirm_reg_password')

    if st.button("Register", key='reg_button'):
        if new_password != confirm_password:
            st.error('Passwords do not match!')
        else:
            alphabets = re.findall(r'[A-Za-z]', new_password)
            numbers = re.findall(r'[0-9]', new_password)
            if new_username and new_password:
                if alphabets and numbers:
                    if len(new_password) < 6:
                        st.error('Password must be at least 6 characters')
                    else:
                        add_user(new_username, new_password, role="User")
                        st.success("🎉 Registration successful! You can now log in.")
                        st.session_state["page"] = "Login"
                        st.rerun()
                else:
                    st.error('Password must contain both letters and numbers')
            else:
                st.error("⚠️ Please fill all fields.")

    if st.button("Back to Login", key='back_to_login'):
        st.session_state["page"] = "Login"
        st.rerun()

# -------------------------------
# Admin Page
# -------------------------------
elif st.session_state["page"] == "Admin":
    admin_dashboard()

# -------------------------------
# User Page
# -------------------------------
elif st.session_state["page"] == "User":
    user = st.session_state.get("user", "Unknown")
    st.markdown(f"<div class='welcome_message'>🎓 Welcome Back {user}</div>", unsafe_allow_html=True)
    
    cgpa_calculator_page()
    
    if st.sidebar.button("Logout"):
        st.session_state.clear()
        st.rerun()
