
import os
import streamlit as st
import google.generativeai as genai

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    st.error("❌ GEMINI_API_KEY not found. Please set environment variable.")
    st.stop()
client = genai.Client(api_key=API_KEY)
model_name = "models/gemini-2.5-flash"

# -----------------------------
# UI
# -----------------------------
st.title("AI Chatbot 🤖 ")

# store chat history
if "chat" not in st.session_state:
    st.session_state.chat = []

# input box
user_input = st.text_input("Ask something:")

# -----------------------------
# RESPONSE GENERATION
# -----------------------------
if user_input:

    # save user message
    st.session_state.chat.append(("You", user_input))

    # build conversation history
    history_text = ""
    for role, text in st.session_state.chat:
        history_text += f"{role}: {text}\n"

    # send to Gemini
    response = client.models.generate_content(
        model=model_name,
        contents=f"""
You are a helpful AI assistant.

Conversation history:
{history_text}

User: {user_input}
Assistant:
"""
    )

    bot_reply = response.text

    # save bot response
    st.session_state.chat.append(("Bot", bot_reply))

# -----------------------------
# DISPLAY CHAT
# -----------------------------
for role, text in st.session_state.chat:
    if role == "You":
        st.write(f"🧑 **You:** {text}")
    else:
        st.write(f"🤖 **Bot:** {text}")