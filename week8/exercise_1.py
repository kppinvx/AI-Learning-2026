from typing import TypedDict

from langchain_google_genai import ChatGoogleGenerativeAI

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from dotenv import load_dotenv

load_dotenv()


# --------------------------------------------------
# 1. State
# --------------------------------------------------

class WorkflowState(TypedDict):
    topic: str
    research: str
    summary: str


# --------------------------------------------------
# 2. Gemini
# --------------------------------------------------

llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    temperature=0
)


# --------------------------------------------------
# 3. Nodes
# --------------------------------------------------

def research_node(state: WorkflowState):

    response = llm.invoke(
        f"""
        Research the following topic conceptually:

        Topic: {state["topic"]}

        Give me 5 important points.
        """
    )

    return {
        "research": response.content
    }


def summary_node(state: WorkflowState):

    response = llm.invoke(
        f"""
        Summarize the following research in 3-4 sentences.

        Research:
        {state["research"]}
        """
    )

    return {
        "summary": response.content
    }


# --------------------------------------------------
# 4. Build graph
# --------------------------------------------------

builder = StateGraph(WorkflowState)

builder.add_node("research", research_node)
builder.add_node("summary", summary_node)

builder.add_edge(START, "research")
builder.add_edge("research", "summary")
builder.add_edge("summary", END)


# --------------------------------------------------
# 5. Enable persistence
# --------------------------------------------------

checkpointer = InMemorySaver()

graph = builder.compile(
    checkpointer=checkpointer
)


# --------------------------------------------------
# 6. Thread ID
# --------------------------------------------------

config = {
    "configurable": {
        "thread_id": "exercise-1"
    }
}


# --------------------------------------------------
# 7. Run
# --------------------------------------------------

result = graph.invoke(
    {
        "topic": "Human-in-the-loop AI agents"
    },
    config=config
)


print("\nFinal result:")
print(result)
