import streamlit as st
from openai import OpenAI, APIError,Timeout,APIConnectionError
from styles import inject_css
# ---------------------------------
# 🔹 Initialize OpenAI Client
# ---------------------------------

# if "msg_count" not in st.session_state:
#     st.session_state.msg_count = 0

# if prompt := st.chat_input("Ask your question..."):
#     if st.session_state.msg_count >= 10:
#         st.warning("⚠️ You’ve reached your free limit for today.")
#     else:
#         st.session_state.msg_count += 1
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ---------------------------------
# 💬 Student Chatbot
# ---------------------------------
def student_chatbot():
    inject_css("general")
    st.title("💬 EduSmart AI Assistant")
    st.markdown("Hey there 👋! I'm your personal AI study buddy. Ask me about **assignments, GPA, or any academic topic!**")

    # 🔹 Style the chat area
    st.markdown("""
    <style>
    .stChatMessage.user {background-color: #e3f2fd; border-radius: 12px; padding: 8px; margin-bottom: 6px;}
    .stChatMessage.assistant {background-color: #f1f8e9; border-radius: 12px; padding: 8px; margin-bottom: 6px;}
    </style>
    """, unsafe_allow_html=True)

    # 🔹 Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # 🔹 Display previous messages
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 🔹 User input field
    if prompt := st.chat_input("Type your question here..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # 🔹 Generate AI response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": (
                                "You are EduSmart, a friendly and knowledgeable AI tutor for students. "
                                "Provide clear, step-by-step explanations and study tips related to courses, GPA, assignments, or academic life."
                            )},
                            *st.session_state.chat_history
                        ],
                    )
                    reply = response.choices[0].message.content
                    st.markdown(reply)
                except APIConnectionError: 
                    st.markdown("Connection not established yet , please contact my developer")

        # 🔹 Save the assistant reply
                    if reply:
                        st.session_state.chat_history.append({"role": "assistant", "content": reply})
                    else:
                        pass
        
