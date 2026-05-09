import streamlit as st
import google.generativeai as genai

# API KEY
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# MODEL
model = genai.GenerativeModel("gemini-2.5-flash")

# UI
st.title("AI Chatbot 🤖")

if "chat" not in st.session_state:
    st.session_state.chat = []

user_input = st.text_input("Ask something:")

if user_input:

    st.session_state.chat.append(("You", user_input))

    history = ""
    for role, text in st.session_state.chat:
        history += f"{role}: {text}\n"

    try:
        response = model.generate_content(
            f"""
You are a helpful AI assistant.

Conversation history:
{history}

User: {user_input}
Assistant:
"""
        )

        bot_reply = response.text

    except Exception as e:
        bot_reply = f"Error: {e}"

    st.session_state.chat.append(("Bot", bot_reply))

for role, text in st.session_state.chat:
    if role == "You":
        st.write(f"🧑 **You:** {text}")
    else:
        st.write(f"🤖 **Bot:** {text}")

