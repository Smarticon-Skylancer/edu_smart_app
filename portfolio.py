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
    st.image(r"C:\Users\hp\Desktop\My_apps\My_Edu_smart_app\WhatsApp Image 2025-11-17 at 00.20.53_839ee808.jpg", width=100)  # replace with your own photo
    
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
        

