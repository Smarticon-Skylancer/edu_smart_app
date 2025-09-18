import streamlit as st
from styles import inject_css
from db import fetch_all_users, remove_user
from courses import load_courses, save_courses
from db import add_announcement, fetch_announcements
import pandas as pd

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
    admin_option = st.sidebar.radio("Navigation", ["Dashboard","Course Records","Student Records", "Add a Course", "Remove a Course", "Add a User", "Remove a User","Post Announcement", "Logout",])

    if admin_option == "Dashboard":
        st.markdown("<div class='admin-title'>📊 Admin Dashboard</div>", unsafe_allow_html=True)
        st.header('Welcome Smart')
        
        
    elif admin_option == "Course Records":
        st.subheader("👨‍🏫 Manage Courses")
        st.dataframe(df_courses)
        
        
    elif admin_option == "Student Records":
        st.header(" 👥 Registered Users")
        users = fetch_all_users()
        if users:
            df = pd.DataFrame(users, columns=["Username", "Department", "Level", "Type of student", "Email", "Role"])
            
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
            st.write('### No Regitered Users yet !!! ')


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
        
        

    elif admin_option == "Remove a User":
        st.subheader("➖ Remove a User")
        users = fetch_all_users()
        df_users = pd.DataFrame(users, columns=["Username", "Department", "Level", "Type of student", "Email", "Role"])
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
