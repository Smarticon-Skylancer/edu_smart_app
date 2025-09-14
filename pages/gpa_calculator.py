import streamlit as st
from styles import inject_css
from courses import load_courses
import pandas as pd

def admin_dashboard():
    inject_css("admin")
    # (paste your admin_dashboard logic here)


def cgpa_calculator_page(user):
    inject_css("general")
    
    df_courses = load_courses()
    st.header("🎓 CGPA Calculator")
    st.markdown("<div class='sub-title'>Select your level, enter grades, and calculate your GPA easily.</div>", unsafe_allow_html=True)
    st.write("---")

    if df_courses.empty:
        st.warning("⚠️ No courses available. Please contact the Admin.")
        return

    level = st.selectbox("📌 Select Your Level:", df_courses["Level"].unique())
    level_courses = df_courses[df_courses["Level"] == level]["Course"].unique().tolist()

    num_courses = st.number_input(
        f"Enter number of courses (Max: {len(level_courses)}):",
        min_value=1, max_value=len(level_courses), step=1
    )

    st.write("### 📚 Enter Your Course Details")
    course_inputs = []
    grade_points = {"A": 5, "B": 4, "C": 3, "D": 2, "E": 1, "F": 0}
    course_summary = []

    selected_courses = []  # Track already chosen courses
    total_credit_units = []

    for i in range(num_courses):
        st.write(f"#### Course {i+1}")

        available_courses = [c for c in level_courses if c not in selected_courses]
        if not available_courses:
            st.warning("⚠️ No more unique courses left to select.")
            break

        course = st.selectbox(f"Select Course {i+1}", available_courses, key=f"course_{i}")
        selected_courses.append(course)

        credit_unit = st.number_input(
            f"Enter Credit Units for {course}",
            min_value=1, max_value=6, step=1, key=f"credit_{i}"
            
        )
        total_credit_units.append(credit_unit)
        grade = st.selectbox(
            f"Enter Grade for {course}",
            options=list(grade_points.keys()), key=f"grade_{i}"
        )

        course_inputs.append({"Course": course, "CreditUnit": credit_unit, "Grade": grade})

    if st.button("🎯 Calculate GPA", key='Calculate_cgpa'):
        # ✅ Validation: prevent duplicates
        courses_list = [c["Course"] for c in course_inputs]
        if len(courses_list) != len(set(courses_list)):
            st.error("⚠️ Duplicate courses detected! Please ensure all courses are unique.")
            return

        total_units = sum([c["CreditUnit"] for c in course_inputs])
        total_points = sum([c["CreditUnit"] * grade_points[c["Grade"]] for c in course_inputs])
        gpa = total_points / total_units if total_units > 0 else 0

        st.write("### 📊 Breakdown of Results")

        # ✅ Start index at 1
        df_display = pd.DataFrame(course_inputs)
        df_display.index = df_display.index + 1
        st.dataframe(df_display)
        
        # Summary Table
        
        st.write("###  Summary of Results : ")
        course_summary.append({'Total Courses Entered': len(courses_list), "Total Credit Units": sum(total_credit_units),"Total Points Attainable": sum(total_credit_units)*5, "Total points Attained": total_points})
        
        summary_table = pd.DataFrame(course_summary)
        # Removing Index
        summary_table.set_index('Total Courses Entered', inplace=True, drop=True)

        st.dataframe(summary_table)


        if gpa >= 4.5:
            st.markdown(f"""<div class ='cgpa-success'>Your GPA is : {gpa:.2f} <br>
                        Class of Degree : First Class</div>""", unsafe_allow_html=True)
        elif gpa >= 3.5:
            st.markdown(f"""<div class ='cgpa-success'>Your GPA is : {gpa:.2f} <br>
                        Class of Degree : Second Class Upper</div>""", unsafe_allow_html=True)
        elif gpa >= 2.5:
            st.markdown(f"""<div class ='cgpa-success'>Your GPA is : {gpa:.2f} <br>
                        Class of Degree : Second Class Lower</div>""", unsafe_allow_html=True)
        elif gpa >= 1.5:
            st.markdown(f"""<div class ='cgpa-success'>Your GPA is : {gpa:.2f} <br>
                        Class of Degree : Third Class</div>""", unsafe_allow_html=True)
        else:
            st.error("Class of Degree : Please check with the school.")