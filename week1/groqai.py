from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.1,
    top_p=0.9,
    max_tokens=500
)

print("Groq Chatbot")
print("Type 'exit' to quit\n")

while True:
    question = input("You: ")

    if question.lower() == "exit":
        break

    response = llm.invoke([
        HumanMessage(content=question)
    ])

    if isinstance(response.content, list):
        text = "".join(
            item.get("text", "")
            for item in response.content
            if item.get("type") == "text"
        )
    else:
        text = response.content

    print(f"\nBot: {text}\n")
    print()
