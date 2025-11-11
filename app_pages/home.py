import streamlit as st
from styles import inject_css

def home_page():
    # -------------------------------
# Homepage
# -------------------------------

    inject_css("home")
    st.markdown("""
            <div style='text-align:center'>
            <h1>🎓 Welcome to Smart GPA Calculator</h1>
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
    """)

    st.write("---")
    col1, col2 = st.columns([1, 1])
    with col1:
        st.button("🔐 Login", use_container_width=True)
        st.session_state["page"] = "Login"
    with col2:
        st.button("📝 Sign Up", use_container_width=True)
        st.session_state["page"] = "Register"
