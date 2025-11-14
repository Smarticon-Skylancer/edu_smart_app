import streamlit as st
from styles import inject_css
from app_pages.ui_helpers import render_sidebar
from db import fetch_all_users, remove_user, tutor_fetch_assignments,add_score,fetch_scores_table
from courses import load_courses, save_courses
from courses import get_courses_by_department, display_courses
from db import add_announcement, fetch_announcements,add_assignment,fetch_submissions,remove_submission, remove_assignment,remove_grades
import pandas as pd


def post_an_assignment():
    st.header("📄 Post a New Assignment")
    faculty = st.session_state.get("faculty")
    department = st.session_state.get("department")
    assigned_by = st.session_state.get("user")

    # Form layout in two columns
    col1, col2 = st.columns([2, 1])
    with col1:
        title = st.text_input("Assignment Title")
        question = st.text_area("Question / Description", height=220, placeholder="Enter assignment details here...")
        course = st.text_input("Course (e.g., BIO101)")
    with col2:
        assignment_id = st.text_input("Assignment ID", placeholder="Unique ID (e.g., A001)")
        level = st.selectbox("Level", [100,200,300,400,500,600])
        assignment_marks = st.number_input("Total Marks", min_value=0)
        dead_line = st.date_input("Submission Deadline")

    if st.button("📩 Post Assignment", use_container_width=True):
        if not all([title, question, course, assignment_id]):
            st.warning("⚠️ Please fill in all required fields: Title, Question, Course, Assignment ID.")
        else:
            try:
                add_assignment(assignment_id, faculty, course, department, level, title, question, assigned_by, dead_line, assignment_marks)
                st.success(f"{title} successfully posted!")
            except Exception as e:
                st.error(f"Could not post assignment: {e}")

    st.write("### 📜 Recent Assignments")
    faculty = st.session_state.get("faculty")
    department = st.session_state.get("department")
    assignments = tutor_fetch_assignments(faculty,department)
    if assignments:
        # show each assignment as a compact card with actions
        for ass in assignments:
            (ass_id, fac, course_name, dept, lvl, title, question, assigned_by, deadline, marks) = ass
            with st.expander(f"{title} — {course_name} ({lvl}) — ID: {ass_id}"):
                st.markdown(f"**Question:** {question}")
                st.markdown(f"**Deadline:** {deadline} &nbsp;&nbsp; **Marks:** {marks} &nbsp;&nbsp; **Assigned by:** {assigned_by}")
                col_a, col_b = st.columns([3,1])
                with col_b:
                    if st.button("Delete", key=f"delete_{ass_id}"):
                        # confirmation step
                        confirm = st.checkbox("I confirm deletion of this assignment", key=f"confirm_del_{ass_id}")
                        if confirm:
                            try:
                                # remove by title & question (db supports this currently)
                                remove_assignment(title, question)
                                st.success("Assignment deleted")
                                try:
                                    st.experimental_rerun()
                                except Exception:
                                    st.stop()
                            except Exception as e:
                                st.error(f"Could not delete: {e}")
    else:
        st.info("No assignments yet.")

def post_an_announcement():
    category = st.selectbox("Select Category:", ['Announcement', 'Event'])

    title = st.text_input("Enter Title")
    message = st.text_area("Enter Message", height=150, placeholder="Enter your message here...")
    
    if st.button("📩 Post", use_container_width=True):
        if not title or not message:
            st.warning("⚠️ Please fill in all fields.")
        else:
            add_announcement(category, title, message, "Admin")
            st.success(f"{category} successfully posted!")

    st.write("### 📜 Recent Posts")
    announcements = fetch_announcements()
    if announcements:
        for ann in announcements:
            st.info(f"**[{ann[0]}] {ann[1]}**\n\n{ann[2]}\n\n*Posted by {ann[3]} on {ann[4]}*")
    else:
        st.write("No announcements yet.")
        
def admin_dashboard():
    inject_css("admin") 

    df_courses = load_courses().sort_values(by=['Level'])
    user = st.session_state.get("user")
    first_name = st.session_state.get("firstname")
    surname = st.session_state.get("surname")
    department = st.session_state.get("department")
    email = st.session_state.get("email")
    faculty = st.session_state.get("faculty")
    tutor_id = st.session_state.get("tutor_ID")

    # Compact, consistent sidebar using helper
    nav_items = ["Dashboard","Course Records","Student Records", "Add a Course", "Remove a Course", "Add a Student", "Remove a Student","Post Announcement","Post Assignments","View Submissions"]
    admin_option = render_sidebar(display_name=f"{first_name} {surname}", role="Tutor", faculty=faculty, department=department, nav_options=nav_items, key_prefix="admin")
    Total_courses = get_courses_by_department()
    Total_students = fetch_all_users(department)
    Total_assigned = tutor_fetch_assignments(faculty,department)
    Total_submissions = fetch_submissions(department,level=None)
    if admin_option == "Dashboard":
        st.title("📊 Course Tutor Dashboard")
        st.markdown(f"<div class='sub-title'>Welcome back, <strong>{first_name} {surname}</strong></div>", unsafe_allow_html=True)

        # Compact metrics row
        c1, c2, c3, c4 = st.columns(4, gap="small")
        c1.metric("Assignments Posted", len(Total_assigned))
        c2.metric("Students", len(Total_students))
        c3.metric("Courses", len(Total_courses))
        c4.metric("Submissions", len(Total_submissions))

        st.markdown("---")
        # Quick info card
        st.markdown(
            f"""
            <div class='user-info-card'>
              <h2>📋 Tutor Overview</h2>
              <p><strong>Full Name:</strong> {first_name} {surname}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<strong>Department:</strong> {department}</p>
              <p><strong>Faculty:</strong> {faculty} &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <strong>Tutor ID:</strong> {tutor_id} </p>
              <p><strong>Email:</strong> {email}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
    
    elif admin_option == "Course Records":
        st.subheader("👨‍🏫 Manage Courses")
        courses_df=get_courses_by_department()
        display_courses(courses_df)
        
    elif admin_option == "Student Records":
        st.header(" 👥 Registered Students")
        department = st.session_state.get("department")
        Students = fetch_all_users(department)
        
        if Students:
            df = pd.DataFrame(Students, columns=["Firstname", "Surname", "Username", "Student_id", "Department", "Level", "Type_of_student", "Email", "Faculty", "Role"])
            
            # Set index properly
            df = df.set_index(pd.RangeIndex(1, len(df) + 1))

            # Apply styling
            styled_df = df.style.set_properties(
                **{
                    'background-color': "#1f2937",
                    'color': 'white'
                }
            )

            # Display styled dataframe
            st.dataframe(styled_df)
        else:
            st.info('ℹ️ No Registered Students yet !!! ')
        st.header(" 🎓 Students Performance")
        department = st.session_state.get("department")
        performance = fetch_scores_table(department)
        
        if performance:
            df = pd.DataFrame(performance, columns = ["Student Name","Department","Assignment Scores","Course"])
            df = df.set_index(pd.RangeIndex(1, len(df) + 1))
            
            # Apply styling
            styled_df = df.style.set_properties(
                **{
                    'background-color': "#1f2937",
                    'color': 'white'
                }
            )
            st.dataframe(styled_df)

            if st.button("Delete Records", key=f"delete"):
                remove_grades()
        else:
            st.info('ℹ️ No Academic Records yet !!! ')


    elif admin_option == "Add a Course":
        st.subheader("➕ Add a Course")
        new_level = st.selectbox("Select Level : ", [100, 200, 300, 400])
        new_course = st.text_input("Course Name").upper()
        department = st.session_state.get("department")
        if st.button("Add Course", key='Add_course', use_container_width=True):
            if new_level and new_course:
                if new_course in df_courses['Course'].values:
                    st.error('⚠️ Course already exists!')
                else:
                    df_courses = pd.concat([df_courses, pd.DataFrame([{"Level": new_level, "Course": new_course, "Department": department}])], ignore_index=True)
                    save_courses(df_courses)
            else:
                st.error("⚠️ Please fill all fields.")

    elif admin_option == "Remove a Course":
        st.subheader("➖ Remove a Course")
        courses_df = get_courses_by_department()
        if not courses_df.empty:
            course_to_remove = st.selectbox("Select course to remove", courses_df["Course"].unique())
            if st.button("Remove Course", key='Remove_course', use_container_width=True):
                courses_df = courses_df[courses_df["Course"] != course_to_remove]
                save_courses(courses_df)
                st.success(f"Course {course_to_remove} removed successfully!")
        else:
            st.info("ℹ️ No courses available to remove.")
            
    elif admin_option == "Post Announcement":
        post_an_announcement()
        
    elif admin_option == "Post Assignments":
        post_an_assignment()
    elif admin_option == "View Submissions":
        department = st.session_state.get("department")
        faculty = st.session_state.get("faculty")
        if faculty == "Health_Sciences":
            level = st.selectbox("Select Level : ", [100, 200, 300, 400,500,600])
        else:
            level = st.selectbox("Select Level : ", [100, 200, 300, 400])
        submissions = fetch_submissions(department,level)
        st.header("Submission Page")
        if submissions:
            # submissions table columns (as created in db):
            # student_id, assignment_id, student_name, department, question, course, level, answers, assignment_marks, date_submitted
            for i, (student_id, assignment_id, student_name, dept, question, course_name, lvl, answers, assignment_marks, date_submitted) in enumerate(submissions, start=1):
                with st.expander(f"📝 {i}. {question} — Answered by {student_name} ({dept}, {lvl})"):
                    st.write(f"**Answers:**")
                    st.write(answers)
                    st.markdown(f"**Date Submitted:** {date_submitted}")
                    st.markdown(f"**Assignment Marks (max):** {assignment_marks}")
                    col1, col2 = st.columns([3,1])
                    with col1:
                        score = st.number_input(f"Enter Score for {student_name}", min_value=0, max_value=assignment_marks, key=f"score_{i}")
                    with col2:
                        if st.button("Submit score", key=f"submit_{assignment_id}"):
                            try:
                                add_score(student_name, dept, score, course_name)
                                st.success(f"✅ {student_name} scored successfully!")
                                # remove submission after scoring
                                remove_submission(question, answers)
                                try:
                                    st.experimental_rerun()
                                except Exception:
                                    st.stop()
                            except Exception as e:
                                st.error(f"Could not save score: {e}")
        else:
            st.info("ℹ️ No Submissions Have been made yet !")
            
    elif admin_option == "Add a Student":
        st.subheader("➕ Add a Student")
        st.info("Feature coming soon!")                           
        
    elif admin_option == "Remove a Student":
        inject_css("admin")
        st.subheader("➖ Remove a Student")
        Students = fetch_all_users(department)
        df_Students = pd.DataFrame(Students, columns=["Firstname", "Surname", "Username", "Student_id", "Department", "Level", "Type_of_student", "Email", "Faculty", "Role"])
        if not df_Students.empty:
            Student_to_remove = st.selectbox("Select Student to remove", df_Students["Username"].unique())
            role = "Student"
            if st.button("Remove Student", key='Remove_Student', use_container_width=True):
                remove_user(Student_to_remove, role)
                st.success(f"{role} {Student_to_remove} removed successfully!")
                import time
                time.sleep(3)
                st.rerun()
                    
        else:
            st.info("ℹ️ No Students available to remove.")
