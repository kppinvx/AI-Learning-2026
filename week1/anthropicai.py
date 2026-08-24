from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage

load_dotenv()

llm = ChatAnthropic(
    model="claude-sonnet-4-6",
    temperature=0.7,
    top_p=0.9,
    top_k=40,
    max_tokens=500
)

print("Anthropic Chatbot")
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
