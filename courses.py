import os
import pandas as pd
import streamlit as st

# Get directory of this file (app/)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# courses.csv inside the same app folder
COURSES_FILE = os.path.join(BASE_DIR, "courses.csv")


def load_courses():
    """
    Load courses into a DataFrame.
    Always returns a DataFrame with columns: Level, Course, Department
    """
    if os.path.exists(COURSES_FILE):
        df = pd.read_csv(COURSES_FILE)
        # Ensure required columns exist
        expected_columns = ["Level", "Course", "Department"]
        for col in expected_columns:
            if col not in df.columns:
                df[col] = None
        df = df[expected_columns]
        # Reset index to start at 1
        df.index = pd.RangeIndex(start=1, stop=len(df) + 1, step=1)
        return df
    else:
        return pd.DataFrame(columns=["Level", "Course", "Department"])


def get_courses_by_department():
    """
    Return courses filtered by department from st.session_state["department"].
    """
    df = load_courses()

    if df.empty:
        return df
    if st.user:
        department = st.session_state.get("department", None)
    else:
        department = st.session_state.get("guest_department", None)

    if department:
        df = df[df["Department"] == department]

    return df


def display_courses(df):
    """Display styled DataFrame in Streamlit."""
    if df.empty:
        st.info("No courses available yet.")
    else:
        styled_df = df.style.set_properties(
            **{
                'background-color': "black",
                'color': 'white',
                'border-color': 'gray'
            }
        )
        st.dataframe(styled_df)


def save_courses(df):
    """Save DataFrame to CSV file."""
    df.to_csv(COURSES_FILE, index=False)
    st.success("✅ Courses saved successfully!")
