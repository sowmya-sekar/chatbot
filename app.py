import streamlit as st
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from dotenv import load_dotenv
load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")
# MODEL via LangChain
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

# PROMPT TEMPLATE via LangChain
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI assistant. If user gives a math expression, calculate it."),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}")
])

# CHAIN via LangChain
chain = prompt | llm

# CALCULATOR TOOL from chatbot.py
def calculator(expression):
    try:
        return str(eval(expression))
    except:
        return "Invalid math expression"

# UI
st.title("AI Chatbot 🤖")

# MEMORY
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "chat" not in st.session_state:
    st.session_state.chat = []

user_input = st.text_input("Ask something:")

if user_input:
    st.session_state.chat.append(("You", user_input))

    try:
        # TOOL CHECK — calculator first!
        if any(op in user_input for op in ["+", "-", "*", "/"]):
            bot_reply = calculator(user_input)

        else:
            # LangChain handles AI response
            response = chain.invoke({
                "chat_history": st.session_state.chat_history,
                "input": user_input
            })
            bot_reply = response.content

            # Add to LangChain memory
            st.session_state.chat_history.append(HumanMessage(content=user_input))
            st.session_state.chat_history.append(AIMessage(content=bot_reply))

    except Exception as e:
        bot_reply = f"Error: {e}"

    st.session_state.chat.append(("Bot", bot_reply))

for role, text in st.session_state.chat:
    if role == "You":
        st.write(f"🧑 **You:** {text}")
    else:
        st.write(f"🤖 **Bot:** {text}")