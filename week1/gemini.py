from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-flash-latest",
    temperature=1,
    top_p=0.9,
    # top_k=40,
    max_output_tokens=500
)

print("Gemini Chatbot")
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
