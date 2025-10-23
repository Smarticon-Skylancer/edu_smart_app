import pandas as pd

import streamlit as st
from styles import inject_css
from app_pages.gpa_calculator import cgpa_calculator_page

from app_pages.timetable import time_table_generator
from db import fetch_announcements,student_fetch_assignments,add_submission,get_user_grade,fetch_submissions

import time

def user_dashboard():
    user = st.session_state.get("user", "Unknown")
    faculty = st.session_state.get("department", "Unknown")
    department = st.session_state.get("faculty", "Unknown")
    email = st.session_state.get("role", "Unknown")
    level = st.session_state.get("level", "Unknown")
    type_of_student = st.session_state.get("type_of_student", "Unknown")

    user_option = st.sidebar.radio("Navigation", ["Dashboard", "Timetable Generator", "GPA Calculator","AI Assistant","Chatroom","Assignments","Make a Submission",  "My Grades","Announcements & Events","Logout"])

    if user_option == "Dashboard":
        inject_css("general")
        st.markdown(f"""
        <div class="user-info-card">
            <h2>🎓 Welcome Back {user}</h2>
            <p><strong>Faculty:</strong> {faculty}</p><hr>
            <p><strong>Department:</strong> {email}</p><hr>
            <p><strong>Level:</strong> {level} Level</p><hr>
            <p><strong>Email:</strong> {department}</p><hr>
            <p><strong>Type of Student:</strong> {type_of_student}</p>
        </div>
        """, unsafe_allow_html=True)

    elif user_option == "Timetable Generator":
        time_table_generator()
    elif user_option == "GPA Calculator":
        cgpa_calculator_page(user)
    elif user_option == "Logout":
        st.session_state.clear()
        st.rerun()
    elif user_option == "Chatroom":
        st.info("Feature coming Soon !!! ")
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
        faculty = st.session_state.get("department")
        department = st.session_state.get("role")
        level = st.session_state.get("level")
        assignments = student_fetch_assignments(faculty,department,level)
        st.title("Assignments ")
        if assignments:
            for i, (title, question, assigned_by, date_posted, dead_line, assignment_marks,course,level) in enumerate(assignments, start=1):
                st.markdown(f"### 📝 {i}. {title}")
                st.write(f"**Question:** {question}")
                st.write(f"**Assigned by:** {assigned_by}")
                st.write(f"**Date Posted:** {date_posted}")
                st.write(f"**Dead line:** {dead_line}")
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
        department = st.session_state.get("role")
        
        score_table = get_user_grade(student_name, department)
        for row in score_table:
            if score_table:
                st.subheader(f"Assignments Results")
                df = pd.DataFrame(score_table, columns=["Student Name", "Department", f"Assignment score","Course"])
                
                # Set index properly
                df = df.set_index(pd.RangeIndex(1, len(df) + 1))
                df = pd.DataFrame([row], columns=["Student Name", "Department", f"Assignment score","Course"])
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
                st.info('### No Records yet !!! ')
    elif user_option == "Make a Submission":
        inject_css("general")
        st.title("📬 Make Submissions")
        faculty = st.session_state.get("department")
        department = st.session_state.get("role")
        level = st.session_state.get("level")
        assignments = student_fetch_assignments(faculty,department,level)
        student_name = st.session_state.get("user")
        department = st.session_state.get("role")
        level = st.session_state.get("level")
        course = st.session_state.get("course")

        if not assignments:
            st.info("No assignments available yet.")
        else:
            st.info("Select Assignments and make Submisssions 📝")
            for i, (title, question, assigned_by, date_posted, deadline, assignment_marks, course,level) in enumerate(assignments, start=1):
                with st.expander(f"📝 {i}. {question} from {department}, {level} level, Marks Attainable : {assignment_marks}, Best Submitted before {deadline}"):
                    answers = st.text_area("Enter Your Answers : ", key=f"answers_{i}")
                    submit = st.button("Submit Assignment", key=f"submit_{i}")
                    if answers and submit :
                        add_submission(student_name, department,level,question,answers,course,assignment_marks)
                        st.write(f"Student_name : {student_name} Department : {department} Level : {level} Question : {question} Answers : {answers} Course : {course} Assignment Marks : {assignment_marks}")
                        st.success("Your Assignment have been Submitted Successfully !")
                        st.rerun()
            
                        
