import streamlit as st
from styles import inject_css
from db import fetch_all_users, remove_user, tutor_fetch_assignments,add_score,fetch_scores_table
from courses import load_courses, save_courses
from db import add_announcement, fetch_announcements,add_assignment,fetch_submissions,remove_submission, remove_assignment,remove_grades
import pandas as pd


def post_an_assignment():
    title = st.text_input("Enter title of Assigment : ")
    dead_line = st.date_input("Enter Dead Line for Submission : ")
    faculty = st.session_state.get("faculty")
    assignment_id = st.number_input(label="Enter Assignment ID : ", placeholder="Enter any number")
    department = st.session_state.get("department")
    level = st.selectbox("Select level : ",[100,200,300,400,500,600])
    assigned_by = st.session_state.get("user")
    course = st.text_input("Enter Course for the Assignment : ")
    assignment_marks = st.number_input("Enter Marks Allocated for this Assignment : ",min_value = 0)
    question = st.text_area("Enter Question", height=300, placeholder="Enter assignment Questions here...")
    if st.button("📩 Post"):
        if not title or not question or not dead_line or not department or not course or not assignment_marks or not level:
            st.warning("⚠️ Please fill in all fields.")
        else:
            add_assignment(title,assignment_id, question, assigned_by,dead_line,assignment_marks,faculty,department,course,level)
            st.success(f"{title} successfully posted!")
    
    st.write("### 📜 Recent Assignments")
    faculty = st.session_state.get("faculty")
    department = st.session_state.get("department")
    assignments = tutor_fetch_assignments(faculty,department)
    if assignments:
        for ass in assignments:
            st.info(f"**[{ass[0]}]**\n\n{ass[1]}\n\n Course : {ass[6]}\n\nPosted by : Tutor {ass[2]} \n\n on {ass[3]} \n\n Total Attainable marks : {ass[5]} \n\n Dead line : {ass[4]}")
            st.warning("You cannot undo this Action, this would erase this assignment from the Students dashboard too !")
            confirmation_button = st.checkbox("I am sure", key=f"confirm_{ass}")
            delete_button = st.button('DELETE', key=f"delete_{ass}")
            if delete_button and confirmation_button:
                remove_assignment(title, question)
                st.success("Assignment Deleted Successfully !")
                st.rerun()
    else:
        st.write("No assignments yet.")

def post_an_announcement():
    category = st.selectbox("Select Category:", ['Announcement', 'Event'])

    title = st.text_input("Enter Title")
    message = st.text_area("Enter Message", height=150, placeholder="Enter your message here...")
    
    if st.button("📩 Post"):
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
    admin_option = st.sidebar.radio("Navigation", ["Dashboard","Course Records","Student Records", "Add a Course", "Remove a Course", "Add a User", "Remove a User","Post Announcement","Post Assignments","View Submissions", "Logout"])
    user = st.session_state.get("user")
    department = st.session_state.get("department")
    email = st.session_state.get("email")
    faculty = st.session_state.get("faculty")
    tutor_id = st.session_state.get("role")
    if admin_option == "Dashboard":
        st.title("📊 Course Tutor Dashboard")
        st.header(f'Welcome {user}')
        st.subheader(f"Faculty : {faculty}")
        st.subheader(f"Department : {department}")
        st.subheader(f"Email : {email}")
        st.subheader(f"Tutor ID : {tutor_id}")
        
        
    
    elif admin_option == "Course Records":
        st.subheader("👨‍🏫 Manage Courses")
        st.dataframe(df_courses)
        
        
    elif admin_option == "Student Records":
        st.header(" 👥 Registered Students")
        department = st.session_state.get("faculty")
        users = fetch_all_users(department)
        
        if users:
            df = pd.DataFrame(users, columns=["Username", "Faculty", "Level", "Type_of_student","Email","Department","Role"])
            
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
            st.info('No Registered Users yet !!! ')
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
            st.info(' No Academic Records yet !!! ')


    elif admin_option == "Add a Course":
        st.subheader("➕ Add a Course")
        new_level = st.selectbox("Select Level : ", [100, 200, 300, 400])
        new_course = st.text_input("Course Name").upper()
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
            for i, (student_name,department,level,question,answers,date_submitted,course,assignment_marks) in enumerate(submissions, start=1):
                with st.expander(f"📝 {i}. {question}  —  Answered by {student_name} from {department}, {level} level"):
                    st.write(f"**Answers:** {answers}")
                    st.markdown(f"**Date Submitted:** {date_submitted}")
                    st.markdown(f"**Assignment Marks:** {assignment_marks}")
                    score = st.number_input(f"Enter Score : ", min_value=0,max_value=assignment_marks, key=f"score_{i}") 
                    submit_btn = st.button("Submit score", key=f"submit_{i}")
                    if submit_btn and score :
                        add_score(student_name,department,score,course)
                        st.success(f"✅ {student_name} scored Sucessfully !")
                        remove_submission(question,answers)
        else:
            st.info("No Submissions Have been made yet !")
            
                    
                
        
    elif admin_option == "Remove a User":
        inject_css("admin")
        st.subheader("➖ Remove a User")
        users = fetch_all_users(faculty)
        df_users = pd.DataFrame(users, columns=["Username", "Faculty", "Level", "Type_of_student","Email","Department","Role"])
        if not df_users.empty:
            user_to_remove = st.selectbox("Select User to remove", df_users["Username"].unique())
            if st.button("Remove User", key='Remove_user'):
                remove_user(user_to_remove)
                st.success(f"User {user_to_remove} removed successfully!")
                import time
                time.sleep(3)
                st.rerun()
        else:
            st.info("No users available to remove.")

    elif admin_option == "Logout":
        st.session_state.clear()
        st.rerun()
