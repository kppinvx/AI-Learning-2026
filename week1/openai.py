from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

load_dotenv()

llm = ChatOpenAI(
    model="gpt-5.5",
    temperature=1,
    top_p=0.9,
    max_completion_tokens=500
)

print("OpenAI Chatbot")
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
