from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    # temperature=0
)

# llm = ChatGroq(
#     model="grok-4.7",
#     temperature=0
# )
