import sqlite3
import bcrypt
import streamlit as st

def init_db():
    conn = sqlite3.connect("uses.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS uses (
            username TEXT PRIMARY KEY,
            password BLOB,
            role TEXT,
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
     conn = sqlite3.connect("uses.db")
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

def add_announcement(category, title, message, posted_by):
    create_announcements_table()  # Ensure table exists
    conn = sqlite3.connect("uses.db")
    c = conn.cursor()
    c.execute("INSERT INTO announcements (category, title, message, posted_by) VALUES (?, ?, ?, ?)",
              (category, title, message, posted_by))
    conn.commit()
    conn.close()

   
def fetch_announcements():
    create_announcements_table()
    conn = sqlite3.connect("uses.db")
    c = conn.cursor()
    c.execute("SELECT category, title, message, posted_by, date_posted FROM announcements ORDER BY date_posted DESC")
    announcements = c.fetchall()
    conn.close()
    return announcements


def add_user(username, password, department, level, type_of_student,email, role="User"):
    conn = sqlite3.connect("uses.db")
    c = conn.cursor()
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    try:
       c.execute("""
    INSERT INTO uses (username, password, department, level, type_of_student, email, role)
    VALUES (?, ?, ?, ?, ?, ?, ?)""",(username, hashed, department, level, type_of_student, email, role))
       conn.commit()
    except sqlite3.IntegrityError:
        st.error("⚠️ Username already exists.")
    conn.close()

def remove_user(username, role="User"):
    conn = sqlite3.connect("uses.db")
    c = conn.cursor()
    try:
        c.execute("DELETE FROM uses WHERE username=? AND role=?", (username, role))
        conn.commit()
    except sqlite3.DatabaseError:
        st.error("⚠️ Username does not exist.")
    conn.close()

def login_user(username, password):
    conn = sqlite3.connect("uses.db")
    c = conn.cursor()
    c.execute("""
        SELECT username, password, department, level, type_of_student, email, role
        FROM uses WHERE username = ?
    """, (username,))
    row = c.fetchone()
    conn.close()

    if row:
        db_username, db_password, dept, lvl, type_stu, email, role = row
        if bcrypt.checkpw(password.encode('utf-8'), db_password):
            return db_username, role, dept, lvl, type_stu, email
    return None, None, None, None, None, None

def login_admin(username, password):
    if username == "Smart" and password == "1234.":
        return username, "Admin"
    return None, None

def fetch_all_users():
    conn = sqlite3.connect("uses.db")
    c = conn.cursor()
    c.execute("SELECT username, department, level, type_of_student,email,role FROM uses")
    uses = c.fetchall()
    conn.close()
    return uses
