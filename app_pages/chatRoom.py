import streamlit as st
import sqlite3
from datetime import datetime
import time
from styles import inject_css

# -------------------------------
# Database setup
# -------------------------------
def init_chat_db():
    conn = sqlite3.connect("chat.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            message TEXT,
            department TEXT,
            faculty TEXT,
            level TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

def add_message(username, message,department,faculty,level):
    conn = sqlite3.connect("chat.db")
    c = conn.cursor()
    c.execute("INSERT INTO messages (username, message,department,faculty,level, timestamp) VALUES (?, ?, ?,?,?,?)",
              (username, message,department,faculty,level,  datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

def get_messages(department,faculty,level):
    conn = sqlite3.connect("chat.db")
    c = conn.cursor()
    c.execute("SELECT username, message, timestamp FROM messages where department = ? and faculty = ? and level = ? ORDER BY id DESC LIMIT 50",(department,faculty,level))
    rows = c.fetchall()
    conn.close()
    return rows[::-1]  # reverse to show oldest first

def get_my_message(username, message):
    conn = sqlite3.connect("chat.db")
    c = conn.cursor()
    c.execute("SELECT username, message, timestamp FROM messages where username = ?, message = ? ORDER BY id DESC LIMIT 50",(username,message))
    rows = c.fetchall()
    conn.close()
    return rows[::-1]  # reverse to show oldest first

# -------------------------------
# Chatroom UI
# -------------------------------
def student_chatroom():
    inject_css("Student")
    st.title("💬 Student Chatroom")
    st.markdown("Chat with your classmates here in real-time!")

    init_chat_db()

    username = st.session_state.get("user", "Anonymous")

    # Auto-refresh every 5 seconds
    st_autorefresh = st.empty()
    st_autorefresh.info("Chat updates every 5 seconds ⏳")

    # Display chat messages
    department = st.session_state.get("role")
    faculty = st.session_state.get("department")

    level = st.session_state.get("level")
    
    messages = get_messages(department, faculty,level)
    chat_container = st.container()
    with chat_container:
        for user, msg, ts in messages:
            st.markdown('<div class="message-card">'f"{user} ({ts}): <br> >>> {msg}", unsafe_allow_html=True)

    # Message input box
    message = st.text_area(placeholder="Type your message here 👇",label="💬 Message : ", key="chat_input")
    send_message = st.button("Send Message", key="send_message")
    if message and send_message:
        add_message(username, message,department,faculty,level)
        st.session_state[message] = ""
        st.rerun()
        