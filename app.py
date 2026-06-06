import streamlit as st
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage

# API KEY
os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")

# MODEL
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

# UI
st.title("AI Chatbot 🤖 (LangChain Version)")

# MEMORY — store as LangChain message objects
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "chat" not in st.session_state:
    st.session_state.chat = []

user_input = st.text_input("Ask something:")

if user_input:
    st.session_state.chat.append(("You", user_input))

    try:
        # Add user message to history
        st.session_state.chat_history.append(HumanMessage(content=user_input))

        # Send full history to AI — LangChain handles it!
        response = llm.invoke(st.session_state.chat_history)
        bot_reply = response.content

        # Add AI reply to history
        st.session_state.chat_history.append(AIMessage(content=bot_reply))

    except Exception as e:
        bot_reply = f"Error: {e}"

    st.session_state.chat.append(("Bot", bot_reply))

for role, text in st.session_state.chat:
    if role == "You":
        st.write(f"🧑 **You:** {text}")
    else:
        st.write(f"🤖 **Bot:** {text}")