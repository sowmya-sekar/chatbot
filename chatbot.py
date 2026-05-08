from langchain_ollama import OllamaLLM

# Load model
llm = OllamaLLM(model="llama3")

# Chat memory
chat_history = []

# Simple calculator tool
def calculator(expression):
    try:
        return str(eval(expression))
    except:
        return "Invalid math expression"

print("AI Agent Started!")
print("Type 'exit' to quit.\n")

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Agent stopped.")
        break

    # TOOL CHECK
    if any(op in user_input for op in ["+", "-", "*", "/"]):
        result = calculator(user_input)
        print("Agent:", result)
        continue

    # MEMORY
    chat_history.append(f"User: {user_input}")

    prompt = "\n".join(chat_history)

    response = llm.invoke(prompt)

    print("Agent:", response)

    chat_history.append(f"Agent: {response}")