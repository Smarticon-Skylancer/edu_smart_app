import streamlit as st
from styles import inject_css

# -------------------
# Sidebar
# -------------------
def about_us():
    inject_css()



# -------------------
# Home Page
# -------------------
    st.title("🚀 My Portfolio")
    st.markdown(
        '''
        <div class="sidebar-logo">
            <svg xmlns="http://www.w3.org/2000/svg" width="70" height="70" viewBox="0 0 100 100" role="img" aria-label="Smart logo">
                <defs>
                    <linearGradient id="g" x1="0" x2="1">
                        <stop offset="0" stop-color="#2563eb" />
                        <stop offset="1" stop-color="#7dd3fc" />
                    </linearGradient>
                </defs>
                <rect rx="18" width="100" height="100" fill="url(#g)" />
                <text x="50" y="58" font-size="48" text-anchor="middle" fill="white" font-family="Inter, Arial">MA</text>
            </svg>
            </div>
        </div>
        '''
        , unsafe_allow_html=True)
    
    st.write("""
    Hi, I'm **Michael Ayuba** 👋  
    I'm passionate about **Python, Data Science, and Building Apps**.  
    This portfolio showcases some of the projects I've been working on.  
    """)

    st.subheader("🛠 Skills")
    st.write("- Python (Pandas, Matplotlib, Streamlit)")
    st.write("- Data Cleaning & Analysis")
    st.write("- Web Apps with Streamlit")
    st.write("- Basics of Data Science & Machine Learning (in progress)")
    

# -------------------
# Projects Page
# -------------------
    st.title("📂 My Projects")

    st.subheader("Python projects")
    st.markdown("[👉 View Code on GitHub](https://github.com/Smarticon-Skylancer/pythonprojects.git)")

    st.subheader("🖼 Web projects")
    st.markdown("[👉 View Code on GitHub](https://github.com/Smarticon-Skylancer/webprojects.git)")

    st.subheader("🏠 Hostel Management System")
    st.markdown("[👉 View Code on GitHub](https://github.com/Smarticon-Skylancer/Hostel-management-system.git)")
    
    st.subheader("📊 Data Science Projects")
    st.markdown("[👉 Veiw Code on Github](https://github.com/Smarticon-Skylancer/Data_science_projects.git)")
    
    st.subheader("🎓 Edu Smart App")
    st.markdown("[👉 Veiw Code on Github](https://github.com/Smarticon-Skylancer/edu_smart_app.git)")
# -------------------
# Contact Page
# -------------------
def contact_dev():
    inject_css()
    st.title("📬 Contact Me")
    st.write("Feel free to reach out!")
    
    st.write("📧 Email: smarticon1000@gmail.com")
    st.write("💼 LinkedIn: [linkedin.com/in/smarticon](https://linkedin.com/in/smarticon)")
    st.write("🐙 GitHub: [https://github.com/Smarticon-Skylancer](https://github.com/sl\sky-lancer)")
    st.write("📱 Whatsapp: +234 904 170 2191")
        

