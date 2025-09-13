import streamlit as st
import pandas as pd
import re
import random 
import matplotlib.pyplot as plt  
from db import init_db, add_user, login_user, login_admin, fetch_all_users, remove_user
from courses import load_courses, save_courses
from styles import inject_css

# -------------------------------
# User Dashboard (CGPA Calculator)
# -------------------------------
def cgpa_calculator_page(user):
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

    num_courses = st.number_input(
        f"Enter number of courses (Max: {len(level_courses)}):",
        min_value=1, max_value=len(level_courses), step=1
    )

    st.write("### 📚 Enter Your Course Details")
    course_inputs = []
    grade_points = {"A": 5, "B": 4, "C": 3, "D": 2, "E": 1, "F": 0}
    course_summary = []

    selected_courses = []  # Track already chosen courses
    total_credit_units = []

    for i in range(num_courses):
        st.write(f"#### Course {i+1}")

        available_courses = [c for c in level_courses if c not in selected_courses]
        if not available_courses:
            st.warning("⚠️ No more unique courses left to select.")
            break

        course = st.selectbox(f"Select Course {i+1}", available_courses, key=f"course_{i}")
        selected_courses.append(course)

        credit_unit = st.number_input(
            f"Enter Credit Units for {course}",
            min_value=1, max_value=6, step=1, key=f"credit_{i}"
            
        )
        total_credit_units.append(credit_unit)
        grade = st.selectbox(
            f"Enter Grade for {course}",
            options=list(grade_points.keys()), key=f"grade_{i}"
        )

        course_inputs.append({"Course": course, "CreditUnit": credit_unit, "Grade": grade})

    if st.button("🎯 Calculate GPA", key='Calculate_cgpa'):
        # ✅ Validation: prevent duplicates
        courses_list = [c["Course"] for c in course_inputs]
        if len(courses_list) != len(set(courses_list)):
            st.error("⚠️ Duplicate courses detected! Please ensure all courses are unique.")
            return

        total_units = sum([c["CreditUnit"] for c in course_inputs])
        total_points = sum([c["CreditUnit"] * grade_points[c["Grade"]] for c in course_inputs])
        gpa = total_points / total_units if total_units > 0 else 0

        st.write("### 📊 Breakdown of Results")

        # ✅ Start index at 1
        df_display = pd.DataFrame(course_inputs)
        df_display.index = df_display.index + 1
        st.dataframe(df_display)
        
        # Summary Table
        
        st.write("###  Summary of Results : ")
        course_summary.append({'Total Courses Entered': len(courses_list), "Total Credit Units": sum(total_credit_units),"Total Points Attainable": sum(total_credit_units)*5, "Total points Attained": total_points})
        
        summary_table = pd.DataFrame(course_summary)
        # Removing Index
        summary_table.set_index('Total Courses Entered', inplace=True, drop=True)

        st.dataframe(summary_table)


        if gpa >= 4.5:
            st.markdown(f"""<div class ='cgpa-success'>Your GPA is : {gpa:.2f} <br>
                        Class of Degree : First Class</div>""", unsafe_allow_html=True)
        elif gpa >= 3.5:
            st.markdown(f"""<div class ='cgpa-success'>Your GPA is : {gpa:.2f} <br>
                        Class of Degree : Second Class Upper</div>""", unsafe_allow_html=True)
        elif gpa >= 2.5:
            st.markdown(f"""<div class ='cgpa-success'>Your GPA is : {gpa:.2f} <br>
                        Class of Degree : Second Class Lower</div>""", unsafe_allow_html=True)
        elif gpa >= 1.5:
            st.markdown(f"""<div class ='cgpa-success'>Your GPA is : {gpa:.2f} <br>
                        Class of Degree : Third Class</div>""", unsafe_allow_html=True)
        else:
            st.error("Class of Degree : Please check with the school.")
            
            


    
    
    
    
    
    
    
        
        
def time_table_generator():
    inject_css("general")
    st.title("📅 Timetable App")
    st.header("🎓 Time Table Generator")

# Step 1: Input subjects with weights
    st.header("Enter Subjects and Weights")
    
    num_subjects = st.number_input("How many subjects?", min_value=1, step=1)

    subjects = {}
    for i in range(num_subjects):
        name = st.text_input(f"Subject {i+1} Name", key=f"name_{i}")
        weight = st.number_input(f"How many times should {name} appear per week?", min_value=1, step=1, key=f"weight_{i}")
        if name:
            subjects[name] = weight

    # Step 2: Days & Study Hours
    days = st.text_input("Enter days (comma separated)", "Monday,Tuesday,Wednesday,Thursday,Friday").split(",")
    study_hours = st.text_input("Enter study hours (comma separated)", "8am-10am,10am-12pm,12pm-1pm,2pm-4pm,4pm-6pm").split(",")

    # Add a shuffle button
    if st.button("🎲 Shuffle & Generate Timetable"):
        subject_pool = []
        for subject, weight in subjects.items():
            subject_pool.extend([subject] * weight)

        random.shuffle(subject_pool)
        total_slots = len(days) * len(study_hours)

        if len(subject_pool) < total_slots:
            subject_pool.extend(["Free"] * (total_slots - len(subject_pool)))
        elif len(subject_pool) > total_slots:
            subject_pool = subject_pool[:total_slots]

        timetable = {}
        index = 0
        for day in days:
            timetable[day.strip()] = {}
            for hour in study_hours:
                timetable[day.strip()][hour.strip()] = subject_pool[index]
                index += 1

        df = pd.DataFrame(timetable)
        st.write("### Your Generated Timetable")
        st.dataframe(df)

        # Save to Excel
        df.to_excel("timetable.xlsx")
        st.download_button("⬇ Download as Excel", open("timetable.xlsx", "rb"), "timetable.xlsx")

        # Save to PDF
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.axis('off')
        table = ax.table(cellText=df.values, colLabels=df.columns, rowLabels=df.index, loc='center')
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1.2, 1.2)
        fig.savefig("timetable.pdf", bbox_inches="tight")
        st.download_button("⬇ Download as PDF", open("timetable.pdf", "rb"), "timetable.pdf")

# -------------------------------
# Admin Dashboard
# -------------------------------
def admin_dashboard():
    inject_css("admin")
    

    df_courses = load_courses().sort_values(by=['Level'])
    admin_option = st.sidebar.radio("Navigation", ["Dashboard", "Add a Course", "Remove a Course","Add a User", "Remove a User", "Logout",])

    if admin_option == "Dashboard":
        st.markdown("<div class='admin-title'>📊 Admin Dashboard</div>", unsafe_allow_html=True)
        st.header('Welcome Smart')
        st.subheader("👨‍🏫 Manage Courses")
        st.dataframe(df_courses)

        st.write("### 👥 Registered Users")
        users = fetch_all_users()
        if users:
            df = pd.DataFrame(users, columns=["Username", "Role"])
            
            # Set index properly
            df = df.set_index(pd.RangeIndex(1, len(df) + 1))

            # Apply styling
            styled_df = df.style.set_properties(
                **{
                    'background-color': "green",
                    'color': 'white'
                }
            )

            # Display styled dataframe
            st.dataframe(styled_df)
        else:
            st.info('No Regitered Users yet !!! ')


    elif admin_option == "Add a Course":
        st.subheader("➕ Add a Course")
        new_level = st.selectbox("Select Level : ", [100, 200, 300, 400])
        new_course = st.text_input("Course Name").capitalize()
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
            
    elif admin_option == "Add a User":
        st.info("Feature is coming Soon !!! ")

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

    if st.button("Don't have an account?   Register as Student", key='reg_button'):
        st.session_state["page"] = "Register"
        st.rerun()

# -------------------------------
# Registration Page
# -------------------------------
elif st.session_state["page"] == "Register":
    inject_css("register")
    st.markdown("<div class='register-title'>📝 Register as User</div>", unsafe_allow_html=True)

    new_username = st.text_input("Choose a Username", key='reg_username')
    department = st.text_input("Enter Department", key='department')
    type_of_student = st.selectbox("Select type of Student : ", ["UG STUDENT", "PGD STUDENT"])
    level = st.selectbox("Select Level:", ["100 level", "200 level","300 level", "400 level", "500 level", "600 level"])
    email = st.text_input("Enter Email ", key = 'email' )
    if email and "@" not in email:
        st.error('Enter a Valid email address !!! ')
    else:
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
                            st.markdown("<div class ='Sucess'>🎉 Registration successful! You can now log in.</div>", unsafe_allow_html = True)
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
    user = st.session_state.get("user")
    
    
    
    
    
    
    
    
    
    user_option = st.sidebar.radio("Navigation", ["Dashboard", "Timetable Generator", "GPA Calculator","Assignments", "Logout",])
    if user_option == "Dashboard":
        st.markdown(f"<div class='welcome_message'>🎓 Welcome Back {user}</div>", unsafe_allow_html=True) 
        inject_css("general")


 

        
        
    elif user_option == "Timetable Generator":
        time_table_generator()
    elif user_option == "GPA Calculator":
        cgpa_calculator_page(user)
    
    if user_option == "Logout":
        st.session_state.clear()
        st.rerun()
