import sqlite3
import bcrypt
import streamlit as st

# ==========================================
# ========== DATABASE INITIALIZATION =======
# ==========================================

def create_submission_table():
    conn = sqlite3.connect("submissions.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS submissions(
            student_id TEXT NOT NULL,
            assignment_id INT NOT NULL,
            student_name TEXT NOT NULL,
            department TEXT NOT NULL,
            question TEXT NOT NULL,
            course TEXT NOT NULL,
            level INT NOT NULL,
            answers TEXT NOT NULL,
            assignment_marks INT NOT NULL,
            date_submitted TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(assignment_id, student_name,student_id)
        )
    """)
    conn.commit()
    conn.close()


def create_announcements_table():
    conn = sqlite3.connect("announcements.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS announcements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT,
            title TEXT,
            message TEXT,
            posted_by TEXT,
            date_posted TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def create_assignments_table():
    conn = sqlite3.connect("assignments.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS assignments(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            assignment_id TEXT UNIQUE NOT NULL,
            faculty TEXT NOT NULL,
            course TEXT NOT NULL,
            department TEXT NOT NULL,
            level INT NOT NULL,
            title TEXT NOT NULL,
            question TEXT NOT NULL,
            assigned_by TEXT NOT NULL,
            dead_line TIMESTAMP,
            assignment_marks INT,
            date_posted TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def init_db():
    conn = sqlite3.connect("students.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS uses (
            firstname TEXT NOT NULL,
            surname TEXT NOT NULL,
            username TEXT PRIMARY KEY UNIQUE,
            student_id TEXT UNIQUE,
            password BLOB NOT NULL,
            role TEXT,
            gender TEXT,
            faculty TEXT NOT NULL,
            department TEXT NOT NULL,
            level INT NOT NULL,
            email TEXT NOT NULL,
            type_of_student TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()
    create_announcements_table()


def init_admin_db():
    conn = sqlite3.connect("tutors.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS tutors(
            firstname TEXT NOT NULL,
            surname TEXT NOT NULL,
            gender TEXT,
            tutor_id TEXT PRIMARY KEY UNIQUE NOT NULL,
            tutor_username TEXT UNIQUE NOT NULL,
            tutor_password BLOB NOT NULL,
            tutor_department TEXT NOT NULL,
            faculty TEXT NOT NULL,
            tutor_email TEXT UNIQUE NOT NULL,
            role TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()
    create_assignments_table()


# ==========================================
# ========== USER MANAGEMENT ===============
# ==========================================

def add_user(firstname, surname, username, student_id, password,role, gender, faculty, department, level,email, type_of_student):
    init_db()
    conn = sqlite3.connect("students.db")
    c = conn.cursor()
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    try:
        c.execute("""
            INSERT INTO uses (firstname, surname, username, student_id, password,role, gender, faculty, department, level,email, type_of_student)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (firstname, surname, username, student_id, hashed, role, gender, faculty, department, level, email, type_of_student))
        conn.commit()
    except sqlite3.IntegrityError as e:
        st.error(f"⚠️ Could not create user: {e}")
    conn.close()


def add_tutor(firstname, surname, gender,tutor_id, tutor_username, tutor_password, tutor_department, faculty,tutor_email,role):

    init_admin_db()
    conn = sqlite3.connect("tutors.db")
    c = conn.cursor()
    hashed = bcrypt.hashpw(tutor_password.encode(), bcrypt.gensalt())
    try:
        c.execute("""
            INSERT INTO tutors (firstname, surname, gender, tutor_id, tutor_username, tutor_password, tutor_department, faculty, tutor_email, role)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (firstname, surname, gender, tutor_id, tutor_username, hashed, tutor_department, faculty, tutor_email, role))
        conn.commit()
    except sqlite3.IntegrityError as e:
        st.error(f"⚠️ Could not create tutor: {e}")
    conn.close()


def remove_user(username, role):
    conn = sqlite3.connect("students.db")
    c = conn.cursor()
    c.execute("DELETE FROM uses WHERE username=? AND role=?", (username, role))
    conn.commit()
    conn.close()

def login_user(username, password):
    conn = sqlite3.connect("students.db")
    c = conn.cursor()
    c.execute("""
        SELECT firstname, surname, username, student_id, password,role, gender, faculty, department, level,email, type_of_student
        FROM uses WHERE username = ?
    """, (username,))
    row = c.fetchone()
    conn.close()

    if row:
        firstname, surname, db_username, db_student_id, db_password, role, db_gender, faculty, dept, lvl, email, type_stu = row
        if bcrypt.checkpw(password.encode('utf-8'), db_password):
            return firstname, surname, db_username, db_student_id, role,db_gender, faculty, dept, lvl, email, type_stu
    return None, None, None, None, None, None, None, None, None, None, None


def login_tutor(tutor_username, tutor_password):
    conn = sqlite3.connect("tutors.db")
    c = conn.cursor()
    c.execute("""
        SELECT firstname, surname, gender,tutor_id, tutor_username, tutor_password, tutor_department, faculty,tutor_email, role 
        FROM tutors WHERE tutor_username = ?
    """, (tutor_username,))
    row = c.fetchone()
    conn.close()

    if row:
        firstname, surname, gender,db_tutor_id, db_tutor_username, tutor_db_password, tutor_department, faculty,tutor_email, role = row
        if bcrypt.checkpw(tutor_password.encode('utf-8'), tutor_db_password):
            return firstname, surname, gender,db_tutor_id, db_tutor_username, tutor_department, faculty,tutor_email,role
    return None, None, None, None, None, None, None, None, None


def fetch_all_users(department):
    conn = sqlite3.connect("students.db")
    c = conn.cursor()
    c.execute("SELECT firstname, surname, username, student_id, department, level, type_of_student, email, faculty, role FROM uses WHERE department = ?", (department,))
    users = c.fetchall()
    conn.close()
    return users


# ==========================================
# ========== ANNOUNCEMENTS =================
# ==========================================

def add_announcement(category, title, message, posted_by):
    create_announcements_table()
    conn = sqlite3.connect("announcements.db")
    c = conn.cursor()
    c.execute("INSERT INTO announcements (category, title, message, posted_by) VALUES (?, ?, ?, ?)",
              (category, title, message, posted_by))
    conn.commit()
    conn.close()


def fetch_announcements():
    create_announcements_table()
    conn = sqlite3.connect("announcements.db")
    c = conn.cursor()
    c.execute("SELECT category, title, message, posted_by, date_posted FROM announcements ORDER BY date_posted DESC")
    announcements = c.fetchall()
    conn.close()
    return announcements


# ==========================================
# ========== ASSIGNMENTS ===================
# ==========================================

def add_assignment(assignment_id,faculty, course, department, level, title, question, assigned_by, dead_line, assignment_marks):
    create_assignments_table()
    conn = sqlite3.connect("assignments.db")
    c = conn.cursor()
    try:
        c.execute("""
            INSERT INTO assignments (assignment_id,faculty, course, department, level, title, question, assigned_by, dead_line, assignment_marks)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (assignment_id,faculty, course, department, level, title, question, assigned_by, dead_line, assignment_marks))
        conn.commit()
    except sqlite3.IntegrityError:
        st.error("⚠️ Assignment ID already exists!")
    conn.close()


def remove_assignment(title, question):
    conn = sqlite3.connect("assignments.db")
    c = conn.cursor()
    c.execute("DELETE FROM assignments WHERE title=? AND question=?", (title, question))
    conn.commit()
    conn.close()


def tutor_fetch_assignments(faculty, department):
    conn = sqlite3.connect("assignments.db")
    c = conn.cursor()
    c.execute("""
        SELECT assignment_id,faculty, course, department, level, title, question, assigned_by, dead_line, assignment_marks
        FROM assignments WHERE faculty = ? AND department = ? ORDER BY date_posted DESC
    """, (faculty, department))
    assignments = c.fetchall()
    conn.close()
    return assignments


def student_fetch_assignments(faculty, department, level):
    conn = sqlite3.connect("assignments.db")
    c = conn.cursor()
    c.execute("""
        SELECT assignment_id,faculty, course, department, level, title, question, assigned_by, dead_line, assignment_marks
        FROM assignments WHERE faculty = ? AND department = ? AND level = ? ORDER BY date_posted DESC
    """, (faculty, department, level))
    assignments = c.fetchall()
    conn.close()
    return assignments


# ==========================================
# ========== SUBMISSIONS ===================
# ==========================================

def add_submission(student_id,assignment_id,student_name, department,question,course, level, answers, assignment_marks):
    create_submission_table()
    conn = sqlite3.connect("submissions.db")
    c = conn.cursor()
    try:
        c.execute("""
            INSERT INTO submissions (student_id, student_name, assignment_id, department, level, question, answers, course, assignment_marks)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (student_id, student_name, assignment_id, department, level, question, answers, course, assignment_marks))
        conn.commit()
    except sqlite3.IntegrityError:
        st.error("⚠️ You have already submitted this assignment!")
    conn.close()


def fetch_submissions(department, level):
    create_submission_table()
    conn = sqlite3.connect("submissions.db")
    c = conn.cursor()
    c.execute("""
        SELECT *
        FROM submissions WHERE department = ? AND level = ? ORDER BY date_submitted DESC
    """, (department, level))
    submissions = c.fetchall()
    conn.close()
    return submissions


def remove_submission(question, answers):
    conn = sqlite3.connect("submissions.db")
    c = conn.cursor()
    c.execute("DELETE FROM submissions WHERE question=? AND answers=?", (question, answers))
    conn.commit()
    conn.close()


# ==========================================
# ========== SCORES ========================
# ==========================================

def scores_table():
    conn = sqlite3.connect("scores.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS scores(
            student_name TEXT,
            department TEXT,
            score INT,
            course TEXT
        )
    """)
    conn.commit()
    conn.close()


def add_score(student_name, department, score, course):
    scores_table()
    conn = sqlite3.connect("scores.db")
    c = conn.cursor()
    c.execute("INSERT INTO scores (student_name, department, score, course) VALUES (?, ?, ?, ?)",
              (student_name, department, score, course))
    conn.commit()
    conn.close()


def fetch_scores_table(department):
    conn = sqlite3.connect("scores.db")
    c = conn.cursor()
    c.execute("SELECT * FROM scores WHERE department = ?", (department,))
    grade_table = c.fetchall()
    conn.close()
    return grade_table


def get_user_grade(student_name, department):
    scores_table()
    conn = sqlite3.connect("scores.db")
    c = conn.cursor()
    c.execute("SELECT * FROM scores WHERE student_name = ? AND department = ?", (student_name, department))
    grade_table = c.fetchall()
    conn.close()
    return grade_table


def remove_grades():
    conn = sqlite3.connect("scores.db")
    c = conn.cursor()
    c.execute("DELETE FROM scores")
    conn.commit()
    conn.close()

