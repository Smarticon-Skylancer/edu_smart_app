import streamlit as st
from styles import inject_css
import pandas as pd

def time_table_generator():
    inject_css("general")
    st.title("📅 Timetable App")
    st.header("🎓 Time Table Generator")

# Step 1: Input subjects with weights
    st.header("Enter Subjects and Weights")
    
    num_subjects = st.number_input("How many subjects?", min_value=1, step=1)

    subjects = {}
    for i in range(num_subjects):
        name = st.text_input(f"Subject {i+1} Name", key=f"name_{i}")
        weight = st.number_input(f"How many times should {name} appear per week?", min_value=1, step=1, key=f"weight_{i}")
        if name:
            subjects[name] = weight

    # Step 2: Days & Study Hours
    days = st.text_input("Enter days (comma separated)", "Monday,Tuesday,Wednesday,Thursday,Friday").split(",")
    study_hours = st.text_input("Enter study hours (comma separated)", "8am-10am,10am-12pm,12pm-1pm,2pm-4pm,4pm-6pm").split(",")

    # Add a shuffle button
    if st.button("🎲 Shuffle & Generate Timetable"):
        subject_pool = []
        for subject, weight in subjects.items():
            subject_pool.extend([subject] * weight)

        total_slots = len(days) * len(study_hours)

        if len(subject_pool) < total_slots:
            subject_pool.extend(["Free"] * (total_slots - len(subject_pool)))
        elif len(subject_pool) > total_slots:
            subject_pool = subject_pool[:total_slots]

        timetable = {}
        index = 0
        for day in days:
            timetable[day.strip()] = {}
            for hour in study_hours:
                timetable[day.strip()][hour.strip()] = subject_pool[index]
                index += 1

        df = pd.DataFrame(timetable)
        st.write("### Your Generated Timetable")
        st.dataframe(df)

        # Save to Excel
        df.to_excel("timetable.xlsx")
        st.button("⬇ Download as Excel", open("timetable.xlsx", "rb"), "timetable.xlsx")