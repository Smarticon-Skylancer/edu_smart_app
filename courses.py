<<<<<<< HEAD
import os
import pandas as pd
import streamlit as st

# Get directory of this file (app/)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# courses.csv inside the same app folder
COURSES_FILE = os.path.join(BASE_DIR, "courses.csv")


def load_courses():
    """Load courses into a DataFrame (always return a DataFrame)."""
    if os.path.exists(COURSES_FILE):
        df = pd.read_csv(COURSES_FILE)
        # Ensure expected columns exist
        df = pd.DataFrame(df, columns=["Level", "Course"])
        # Set index to start at 1
        df.index = pd.RangeIndex(start=1, stop=len(df) + 1, step=1)
        return df
    else:
        # Return empty DataFrame if file doesn’t exist yet
        return pd.DataFrame(columns=["LEVEL", "COURSE CODE"])


def display_courses(df):
    """Display styled DataFrame in Streamlit (visual only)."""
    if df.empty:
        st.info("No courses available yet.")
    else:
        styled_df = df.style.set_properties(
            **{
                'background-color': "black",
                'color': 'white'
            }
        )
        st.dataframe(styled_df)


def save_courses(df):
    """Save DataFrame to CSV file."""
    df.to_csv(COURSES_FILE, index=False)
=======
import os
import pandas as pd
import streamlit as st

# Get directory of this file (app/)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# courses.csv inside the same app folder
COURSES_FILE = os.path.join(BASE_DIR, "courses.csv")


def load_courses():
    """Load courses into a DataFrame (always return a DataFrame)."""
    if os.path.exists(COURSES_FILE):
        df = pd.read_csv(COURSES_FILE)
        # Ensure expected columns exist
        df = pd.DataFrame(df, columns=["Level", "Course"])
        # Set index to start at 1
        df.index = pd.RangeIndex(start=1, stop=len(df) + 1, step=1)
        return df
    else:
        # Return empty DataFrame if file doesn’t exist yet
        return pd.DataFrame(columns=["LEVEL", "COURSE CODE"])


def display_courses(df):
    """Display styled DataFrame in Streamlit (visual only)."""
    if df.empty:
        st.info("No courses available yet.")
    else:
        styled_df = df.style.set_properties(
            **{
                'background-color': "black",
                'color': 'white'
            }
        )
        st.dataframe(styled_df)


def save_courses(df):
    """Save DataFrame to CSV file."""
    df.to_csv(COURSES_FILE, index=False)
>>>>>>> a6fa92601b6bbd4c60e4c68f63566b0af936ba0a
