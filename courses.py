import os
import pandas as pd

# Get directory of this file (app/)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# courses.csv inside the same app folder
COURSES_FILE = os.path.join(BASE_DIR, "courses.csv")

def load_courses():
    if os.path.exists(COURSES_FILE):
        return pd.read_csv(COURSES_FILE)
    else:
        # return empty DataFrame if file doesn’t exist yet
        return pd.DataFrame(columns=["Level","Course Code"])

def save_courses(df):
    df.to_csv(COURSES_FILE, index=False)
