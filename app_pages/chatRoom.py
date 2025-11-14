import streamlit as st
import sqlite3
from datetime import datetime
import time
import html as _html
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
    c.execute("SELECT username, message, timestamp FROM messages WHERE username = ? AND message = ? ORDER BY id DESC LIMIT 50", (username, message))
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
    st_autorefresh.info("Chat — click Refresh to update. Auto-refresh is not enabled in this build.")

    # Display chat messages — fix: use correct session keys for department/faculty
    department = st.session_state.get("department")
    faculty = st.session_state.get("faculty")
    level = st.session_state.get("level")

    messages = get_messages(department, faculty, level)
    chat_container = st.container()
    with chat_container:
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        for user, msg, ts in messages:
            # escape message text
            safe_msg = _html.escape(msg)
            safe_user = _html.escape(user)
            # derive initials for avatar
            initials = "".join([p[0] for p in safe_user.split()][:2]).upper()
            is_self = (safe_user == (username or "Anonymous"))
            # layout left/right
            side_class = "msg-right" if is_self else "msg-left"
            bubble_class = "msg-bubble msg-user" if is_self else "msg-bubble msg-other"
            # timestamp formatted
            try:
                ts_display = datetime.strptime(ts, "%Y-%m-%d %H:%M:%S").strftime("%b %d %H:%M")
            except Exception:
                ts_display = ts

            if is_self:
                # user message on right
                html = f"""
                <div class='msg-row {side_class}'>
                  <div style='display:flex;flex-direction:row;align-items:flex-end;gap:.6rem;'>
                    <div class="{bubble_class}">{safe_msg}</div>
                    <div class='msg-avatar' style='background:linear-gradient(90deg,var(--primary),var(--accent));'>{initials}</div>
                  </div>
                </div>
                <div class='msg-meta' style='text-align:right'>{ts_display}</div>
                """
            else:
                # other user message on left
                html = f"""
                <div class='msg-row {side_class}'>
                  <div style='display:flex;flex-direction:row;align-items:flex-start;gap:.6rem;'>
                    <div class='msg-avatar' style='background:#94a3b8'>{initials}</div>
                    <div class="{bubble_class}"><strong style='font-size:0.95rem'>{safe_user}</strong><br>{safe_msg}</div>
                  </div>
                </div>
                <div class='msg-meta' style='text-align:left'>{ts_display}</div>
                """

            st.markdown(html, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Ensure the session key exists before creating the widget (avoids post-instantiation mutation errors)
    if "chat_input" not in st.session_state:
        st.session_state["chat_input"] = ""

    # Message input box (binds to session state)
    message = st.text_area(placeholder="Type your message here 👇", label="💬 Message : ", key="chat_input", value=st.session_state.get("chat_input", ""))
    col1, col2 = st.columns([3,1], gap='small')
    with col2:
        if st.button("Refresh", key="chat_refresh"):
            try:
                st.experimental_rerun()
            except Exception:
                # Fallback: stop the script to allow the UI to refresh next run
                st.stop()

    # Use a callback to send message so we modify session_state inside the callback (allowed)
    def _send_chat_cb(username_arg, dept_arg, fac_arg, level_arg):
        msg = st.session_state.get("chat_input", "").strip()
        if not msg:
            return
        add_message(username_arg, msg, dept_arg, fac_arg, level_arg)
        # Clear the input (this runs inside the callback, which is safe)
        st.session_state["chat_input"] = ""
        try:
            st.experimental_rerun()
        except Exception:
            st.stop()

    send_message = col1.button("Send Message", key="send_message", use_container_width=True,
                              on_click=_send_chat_cb, args=(username, department, faculty, level))
        