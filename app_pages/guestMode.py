from styles import inject_css
import streamlit as st
from app_pages.timetable import time_table_generator
from app_pages.gpa_calculator import cgpa_calculator_page



def guest_page():
    # ------------------------------
# Guest Mode Page
# ------------------------------

    st.markdown("<h2 style='text-align:center;'>👤 Guest Mode</h2>", unsafe_allow_html=True)
    st.markdown(
        """
        <p style="font-size:17px; text-align:center;">
            Use our essential tools instantly without creating an account.  
            No data is saved — everything runs immediately and privately for your convenience.
        </p>
        """,
        unsafe_allow_html=True
    )

    st.write("---")

    # -------- GPA CALCULATOR SECTION --------
    st.subheader("🎓 GPA Calculator")
    st.markdown(
        """
        <p style="font-size:16px;">
        Easily calculate your GPA without signing up.  
        Just enter your courses, credit units, and grades — and get your GPA instantly.
        Perfect for quick checks and fast results.
        </p>
        """,
        unsafe_allow_html=True
    )
    if st.button("Open GPA Calculator", key="guest_to_gpa", use_container_width=True,):
        st.session_state["page"] = "GPA Calculator"
        cgpa_calculator_page(user = False)
        st.rerun()



    st.write("---")

    # -------- TIMETABLE GENERATOR SECTION --------
    st.subheader("📅 Timetable Generator")
    st.markdown(
        """
        <p style="font-size:16px;">
        Create a personalized study timetable in seconds.  
        Select your courses and available hours — the system will generate a clean, organized schedule.
        No login required, no data stored.
        </p>
        """,
        unsafe_allow_html=True
    )

    st.button("Open Timetable Generator", key="guest_to_timetable", use_container_width=True, on_click=lambda : st.session_state.update("Timetable"))
    st.rerun()

    st.write("---")
    # -------- BACK TO LOGIN BUTTON --------

    st.button("Back to Login", key="guest_to_login", use_container_width=True, on_click=lambda: st.session_state.update("Login"))
    st.rerun()

    