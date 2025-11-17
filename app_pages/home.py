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
    col1, col2,col3 = st.columns([1, 1,1], gap= 'small')
    with col1:
        st.button("🔐 Login",key="home_to_login", use_container_width=True, on_click=lambda : st.session_state.update({"page" : "Login"}))
    with col2:
        st.button("📝 Register", use_container_width=True, on_click=lambda: st.session_state.update({"page": "Register"}), key="home_to_register")
    st.markdown("""
<p style='font-size:17px; text-align:center;'>
   Start learning smarter — no login required.
Guest Mode gives you quick access to tools that help you plan your studies, track your grades, and stay on top of your academic goals.
Everything runs instantly and privately for your convenience.
</p>
""", unsafe_allow_html=True)

    with col3:
        st.button("👥 Enter Guest Mode", use_container_width=True, on_click=lambda: st.session_state.update({"page": "Guest"}), key="Guest_mode_button")
        
    st.session_state.update({"page" :"Home"})