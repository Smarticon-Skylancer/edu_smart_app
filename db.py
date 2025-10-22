import sqlite3
import bcrypt
import streamlit as st
def create_submission_table():
    conn = sqlite3.connect("submissions.db")
    c = conn.cursor()
    c.execute("""
              CREATE TABLE IF NOT EXISTS submissions(
               student_name TEXT,
               department TEXT,
               question TEXT,
               course TEXT,
               level INT,
               answers TEXT,
               assignment_marks,
               date_submitted TIMESTAMP DEFAULT CURRENT_TIMESTAMP   
              )""")
    conn.commit()
    conn.close()
def init_db():
    conn = sqlite3.connect("students.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS uses (
            username TEXT PRIMARY KEY,
            password BLOB,
            role TEXT,
            faculty TEXT,
            department TEXT,
            level INT,
            email TEXT,
            type_of_Student TEXT
        )
    """)
    conn.commit()
    conn.close()
    create_announcements_table()
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
     
def init_admin_db():
     conn = sqlite3.connect("tutors.db")
     c = conn.cursor()
     c.execute("""
        CREATE TABLE IF NOT EXISTS tutors(
            tutor_id TEXT PRIMARY KEY,
            tutor_username TEXT,
            tutor_password BLOB,
            tutor_department TEXT,
            faculty TEXT,
            role TEXT,
            tutor_email TEXT
            
        )
    """)
     conn.commit()
     conn.close()
     create_assignments_table()
def create_assignments_table():
    conn = sqlite3.connect("assignments.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS assignments(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            faculty TEXT,
            course TEXT,
            department TEXT,
            level INT,
            title TEXT,
            question TEXT,
            assigned_by TEXT,
            dead_line TIMESTAMP,
            assignment_marks INT,
            date_posted TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def add_announcement(category, title, message, posted_by):
    create_announcements_table()  # Ensure table exists
    conn = sqlite3.connect("announcements.db")
    c = conn.cursor()
    c.execute("INSERT INTO announcements (category, title, message, posted_by) VALUES (?, ?, ?, ?)",
              (category, title, message, posted_by))
    conn.commit()
    conn.close()

def add_assignment(title, question, assigned_by,dead_line,assignment_marks,faculty,department,course,level):
    create_assignments_table()  # Ensure table exists
    conn = sqlite3.connect("assignments.db")
    c = conn.cursor()
    c.execute("INSERT INTO assignments (title, question, assigned_by,dead_line,assignment_marks,faculty,department,course,level) VALUES (?, ?, ?, ?,?,?,?,?,?)",
              (title, question, assigned_by,dead_line,assignment_marks,faculty,department,course,level))
    conn.commit()
    conn.close()
    
    
def add_submission(student_name, department,level,question,answers,course,assignment_marks):
    create_submission_table()
    conn = sqlite3.connect("submissions.db")
    c = conn.cursor()
    c.execute("INSERT INTO submissions (student_name,department,level,question,answers,course,assignment_marks) VALUES (?, ?, ?, ?, ?,?,?)",
              (student_name,department,level,question,answers,course,assignment_marks))
    conn.commit()
    conn.close()
    
def fetch_submissions(department,level):
    create_submission_table()
    conn = sqlite3.connect("submissions.db")
    c = conn.cursor()
    c.execute("SELECT student_name,department,level,question,answers,date_submitted,course,assignment_marks FROM submissions where department = ? and level = ? ORDER BY date_submitted",(department,level))
    submissions = c.fetchall()
    conn.close()
    return submissions
    
    
def fetch_announcements():
    create_announcements_table()
    conn = sqlite3.connect("announcements.db")
    c = conn.cursor()
    c.execute("SELECT category, title, message, posted_by, date_posted FROM announcements ORDER BY date_posted DESC")
    announcements = c.fetchall()
    conn.close()
    return announcements

def add_user(username, password,faculty, department, level, type_of_student,email, role="User"):
    conn = sqlite3.connect("students.db")
    c = conn.cursor()
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    try:
       c.execute("""
    INSERT INTO uses (username, password,faculty, department, level, type_of_student,email, role)
    VALUES (?, ?, ?, ?, ?, ?, ?,?)""",(username, hashed,faculty, department, level, type_of_student,email, role))
       conn.commit()
    except sqlite3.IntegrityError:
        st.error("⚠️ Username already exists.")
    conn.close()

def add_tutor(tutor_username, tutor_password, tutor_department, faculty, tutor_ID,tutor_email, role="Tutor"):
    conn = sqlite3.connect("tutors.db")
    c = conn.cursor()
    hashed = bcrypt.hashpw(tutor_password.encode(), bcrypt.gensalt())
    try:
       c.execute("""
    INSERT INTO tutors (tutor_username, tutor_password, tutor_department, tutor_ID, faculty, tutor_email, role)
    VALUES (?, ?, ?, ?, ?, ?, ?)""",(tutor_username, hashed, tutor_department, tutor_ID, faculty,tutor_email, role))
       conn.commit()
    except sqlite3.IntegrityError:
        st.error("⚠️ Tutor already exists.")
    conn.close()


def remove_user(username, role="User"):
    conn = sqlite3.connect("students.db")
    c = conn.cursor()
    try:
        c.execute("DELETE FROM uses WHERE username=? AND role=?", (username, role))
        conn.commit()
    except sqlite3.DatabaseError:
        st.error("⚠️ Username does not exist.")
    conn.close()

def login_user(username, password):
    conn = sqlite3.connect("students.db")
    c = conn.cursor()
    c.execute("""
        SELECT username, password, department, level, type_of_student, email, role,faculty
        FROM uses WHERE username = ?
    """, (username,))
    row = c.fetchone()
    conn.close()

    if row:
        db_username, db_password, dept, lvl, type_stu, email,fac, role = row
        if bcrypt.checkpw(password.encode('utf-8'), db_password):
            return db_username, role, dept, lvl, type_stu, email,fac
    return None, None, None, None, None, None,None

    return None, None
def login_tutor(tutor_username, tutor_password):
    conn = sqlite3.connect("tutors.db")
    c = conn.cursor()
    c.execute("""
        SELECT tutor_username, tutor_password, tutor_department, tutor_ID, tutor_email, role,faculty
        FROM tutors WHERE tutor_username = ?
    """, (tutor_username,))
    row = c.fetchone()
    conn.close()

    if row:
        db_username, db_password, tutor_dept, tutor_faculty, tutor_email,tutor_ID, role = row
        if bcrypt.checkpw(tutor_password.encode('utf-8'), db_password):
            return db_username, role, tutor_dept, tutor_faculty, tutor_email,tutor_ID
    return None, None, None, None, None, None

    return None, None
def fetch_all_users():
    conn = sqlite3.connect("students.db")
    c = conn.cursor()
    c.execute("SELECT username, department, level, type_of_student,email,faculty,role FROM uses")
    uses = c.fetchall()
    conn.close()
    return uses

def tutor_fetch_assignments(faculty, department):
    conn = sqlite3.connect("assignments.db")
    c = conn.cursor()
    c.execute("SELECT title, question, assigned_by, date_posted,dead_line,assignment_marks,course FROM assignments where faculty = ? and department = ? ORDER BY date_posted DESC ",(faculty, department))
    assignments = c.fetchall()
    conn.close()
    return assignments

def student_fetch_assignments(faculty,department,level):
    conn = sqlite3.connect("assignments.db")
    c = conn.cursor()
    c.execute("SELECT title, question, assigned_by, date_posted,dead_line,assignment_marks,course,level FROM assignments where faculty = ? and department = ? and level = ? ORDER BY date_posted DESC ",(faculty, department,level))
    assignments = c.fetchall()
    conn.close()
    return assignments

def scores_table():
    conn = sqlite3.connect("scores.db")
    c = conn.cursor()
    c.execute("""
              CREATE TABLE IF NOT EXISTS scores(
                student_name TEXT,
                department TEXT,
                score INT,
                course TEXT
                )""")
    conn.commit()
    conn.close()

def add_score(student_name,department,score,course):
    scores_table()
    conn = sqlite3.connect("scores.db")
    c = conn.cursor()
    c.execute("INSERT INTO scores (student_name,department,score,course) VALUES (?, ?, ?, ?)",
              (student_name,department,score,course))
    conn.commit()
    conn.close()


def fetch_scores_table():
    conn = sqlite3.connect("scores.db")
    c = conn.cursor()
    c.execute("""
              SELECT * FROM scores""")
    grade_table = c.fetchall()
    conn.close()
    return grade_table

def remove_submission(question, answers):
    conn = sqlite3.connect("submissions.db")
    c = conn.cursor()
    c.execute("DELETE FROM submissions WHERE question=? AND answers=?", (question, answers))
    conn.commit()
    conn.close()
    
def remove_assignment(title, question):
    conn = sqlite3.connect("assignments.db")
    c = conn.cursor()
    c.execute("DELETE FROM assignments WHERE title=? AND question=?", (title, question))
    conn.commit()
    conn.close()
def get_user_grade(student_name, department):
    scores_table()
    conn = sqlite3.connect("scores.db")
    c = conn.cursor()
    c.execute("SELECT * FROM scores where student_name = ? and department = ?",(student_name, department))
    grade_table = c.fetchall()
   
    conn.close()
    return grade_table

def remove_grades():
    conn = sqlite3.connect("scores.db")
    c = conn.cursor()
    c.execute("DELETE FROM scores")
    conn.commit()
    conn.close()
    
