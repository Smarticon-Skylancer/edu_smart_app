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
            role TEXT
        )
    """)
    conn.commit()
    conn.close()

def add_user(username, password, role="User"):
    conn = sqlite3.connect("uses.db")
    c = conn.cursor()
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    try:
        c.execute("INSERT INTO uses (username, password, role) VALUES (?, ?, ?)",
                  (username, hashed, role))
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
    c.execute("SELECT username, password, role FROM uses WHERE username=?", (username,))
    result = c.fetchone()
    conn.close()
    if result:
        stored_username, stored_password, role = result
        if bcrypt.checkpw(password.encode(), stored_password):
            return stored_username, role
    return None, None

def login_admin(username, password):
    if username == "Smart" and password == "1234.":
        return username, "Admin"
    return None, None

def fetch_all_users():
    conn = sqlite3.connect("uses.db")
    c = conn.cursor()
    c.execute("SELECT username, role FROM uses")
    uses = c.fetchall()
    conn.close()
    return uses
