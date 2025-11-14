import pandas as pd

import streamlit as st
from styles import inject_css
from app_pages.gpa_calculator import cgpa_calculator_page
from app_pages.chatbot import student_chatbot
from app_pages.timetable import time_table_generator
from db import fetch_announcements,student_fetch_assignments,add_submission,get_user_grade,fetch_submissions
from app_pages.chatRoom import student_chatroom
import time
from app_pages.ui_helpers import render_sidebar

def user_dashboard():
    # Ensure global styles are injected for this page (UI-only change)
    inject_css("general")

    user = st.session_state.get("user", "Unknown")
    faculty = st.session_state.get("faculty", "Unknown")
    department = st.session_state.get("department", "Unknown")
    email = st.session_state.get("email", "Unknown")
    level = st.session_state.get("level", "Unknown")
    type_of_student = st.session_state.get("type_of_student", "Unknown")
    firstname = st.session_state.get("firstname", "Unknown")
    surname = st.session_state.get("surname", "Unknown")

    # Build compact sidebar and get selected option
    nav_items = ["Dashboard", "Timetable Generator", "GPA Calculator", "AI Assistant", "Chatroom", "Assignments", "Make a Submission", "My Grades", "Announcements & Events"]
    user_option = render_sidebar(display_name=f"{firstname} {surname}", role="Student", faculty=faculty, department=department, nav_options=nav_items, key_prefix="student")

    if user_option == "Dashboard":
        inject_css("general")

        # Gather quick stats
        announcements = fetch_announcements()
        assignments = student_fetch_assignments(faculty, department, level)
        ann_count = len(announcements) if announcements else 0
        assign_count = len(assignments) if assignments else 0

        st.markdown(f"<div class='sub-title'>Welcome back, <strong>{firstname} {surname}</strong></div>", unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns(4, gap="small")
        c1.metric("Faculty", faculty)
        c2.metric("Department", department)
        c3.metric("Assignments", assign_count)
        c4.metric("Announcements", ann_count)

        st.markdown("---")
        st.markdown(
            f"""
            <div class='user-info-card'>
              <h2>🎓 {user}</h2>
              <p><strong>Full Name:</strong> {firstname} {surname}</p>
              <p><strong>Level:</strong> {level} Level &nbsp; <strong>Type:</strong> {type_of_student}</p>
              <p><strong>Email:</strong> {email}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    elif user_option == "Timetable Generator":
        time_table_generator()
    elif user_option == "GPA Calculator":
        cgpa_calculator_page(user)
    elif user_option == "Chatroom":
        student_chatroom()
    elif user_option == "Announcements & Events":
        inject_css("general")
        st.subheader("📢 Latest Announcements")
        announcements = fetch_announcements()
        if announcements:
            for ann in announcements:
                st.success(f"**[{ann[0]}] {ann[1]}**\n\n{ann[2]}\n\n*Posted by {ann[3]} on {ann[4]}*")
        else:
            st.info("No announcements yet.")
    elif user_option == "Assignments":
        inject_css("general")
        # Correctly read faculty/department/level from session state
        faculty = st.session_state.get("faculty")
        department = st.session_state.get("department")
        level = st.session_state.get("level")
        assignments = student_fetch_assignments(faculty, department, level)
        st.title("Assignments ")
        if assignments:
            # assignment tuple: (assignment_id, faculty, course, department, level, title, question, assigned_by, dead_line, assignment_marks)
            for i, (assignment_id, fac, course_name, dept, lvl, title, question, assigned_by, deadline, assignment_marks) in enumerate(assignments, start=1):
                st.markdown(f"### 📝 {i}. {title}")
                st.write(f"**Course:** {course_name} — **Level:** {lvl}")
                st.write(f"**Question:** {question}")
                st.write(f"**Assigned by:** {assigned_by}")
                st.write(f"**Deadline:** {deadline}")
                st.write(f"**Total Marks Attainable:** {assignment_marks}")
                st.write("---")
        else:
            st.info("No Assignments yet!")
    elif user_option == "AI Assistant":
        student_chatbot()
    elif user_option == "My Grades":
        st.title("🎓 My Grades and Performance")
        inject_css("general")
        student_name = st.session_state.get("user")
        department = st.session_state.get("department")

        score_table = get_user_grade(student_name, department)
        if score_table:
            st.subheader("Assignments Results")
            df = pd.DataFrame(score_table, columns=["Student Name", "Department", "Assignment score", "Course"])
            # Set a readable 1-based index
            df.index = pd.RangeIndex(1, len(df) + 1)
            # Apply simple styling for dark background cards
            styled_df = df.style.set_properties(**{"background-color": "#1f2937", 'color': 'white'})
            st.dataframe(styled_df)
        else:
            st.info("No Records yet !!! ")
    elif user_option == "Make a Submission":
        inject_css("general")
        st.title("📬 Make Submissions")
        # Read correct session values
        faculty = st.session_state.get("faculty")
        department = st.session_state.get("department")
        level = st.session_state.get("level")
        assignments = student_fetch_assignments(faculty, department, level)
        student_name = st.session_state.get("user")
        course = st.session_state.get("course")

        if not assignments:
            st.info("No assignments available yet.")
        else:
            st.info("Select Assignments and make Submisssions 📝")
            # assignment tuple: (assignment_id, faculty, course, department, level, title, question, assigned_by, dead_line, assignment_marks)
            for i, (assignment_id, fac, course_name, dept, lvl, title, question, assigned_by, deadline, assignment_marks) in enumerate(assignments, start=1):
                with st.expander(f"📝 {i}. {title} — {course_name} ({lvl} level) — Marks: {assignment_marks}"):
                    st.write(f"**Question:** {question}")
                    st.write(f"**Assigned by:** {assigned_by}")
                    st.write(f"**Deadline:** {deadline}")
                    answers = st.text_area("Enter Your Answers : ", key=f"answers_{assignment_id}")
                    submit = st.button("Submit Assignment", key=f"submit_{assignment_id}", use_container_width=True)
                    if answers and submit:
                        # Prepare correct parameters for add_submission(student_id,assignment_id,student_name, department,question,course, level, answers, assignment_marks)
                        student_id = st.session_state.get("student_id") or st.session_state.get("user")
                        try:
                            add_submission(student_id, assignment_id, student_name, department, question, course_name, lvl, answers, assignment_marks)
                            st.success("Your Assignment has been submitted successfully!")
                        except Exception as e:
                            st.error(f"Submission failed: {e}")
                        # Refresh safely
                        try:
                            st.experimental_rerun()
                        except Exception:
                            st.session_state["page"] = "Dashboard"
                            st.stop()
            
                        
