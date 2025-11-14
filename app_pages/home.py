import streamlit as st
from styles import inject_css

def home_page():
    # -------------------------------
# Homepage
# -------------------------------

    inject_css("home")
    st.markdown("""
            <div style='text-align:center'>
            <h1>🎓 Welcome to Edu Smart App</h1>
            <p style='font-size:18px; color:#555;'>
                Your all-in-one education assistant for managing grades, calculating GPA,
                and tracking your academic performance with ease.
            </p>
            <hr/>
        </div>
    """, unsafe_allow_html=True)

    st.write("## 📘 Features")
    st.markdown("""
    - 📊 **GPA Calculator** – Compute your GPA accurately for each semester.  
    - 🧮 **Course Manager** – Add or view your registered courses.  
    - 👨‍🏫 **Admin Panel** – Manage courses and users easily. 
    - ⚒️ **Assignment System**  – Make and Submit Assignments seamlessly.
    - 🔒 **Secure Login & Registration** – Keep your records private.  
    - 💡 **User-Friendly Interface** – Simple and modern layout.
    - 📢 **Announcements & Events** – Stay updated with the latest news.
    - 🤖 **AI Assistant** – Get help with your academic queries.
    - 🗓️ **Timetable Generator** – Organize your class schedule efficiently.
    - 💬 **Chatroom** – Connect and collaborate with peers and tutors.
    - 📝 **Grade Tracking** – Monitor your academic progress over time.
    - 🔔 **Notifications** – Receive timely alerts for assignments and events.
    """)

    st.write("---")
    col1, col2 = st.columns([1, 1], gap= 'small')
    with col1:
        if st.button("🔐 Login", use_container_width=True):
            st.session_state["page"] = "Login"
    with col2:
        if st.button("📝 Sign Up", use_container_width=True):
            st.session_state["page"] = "Register"
