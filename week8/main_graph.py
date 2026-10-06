from typing import TypedDict

from langchain_google_genai import ChatGoogleGenerativeAI

from langgraph.graph import StateGraph, START, END

from research_graph import research_graph

from dotenv import load_dotenv

load_dotenv()


# --------------------------------------------------
# Main graph state
# --------------------------------------------------

class MainState(TypedDict):
    topic: str
    research_summary: str
    final_answer: str


llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    temperature=0
)


# --------------------------------------------------
# Final writer
# --------------------------------------------------

def final_writer(state: MainState):

    response = llm.invoke(
        f"""
        You are a senior technical writer.

        Based on the research below, produce a clear
        final answer.

        Topic:
        {state["topic"]}

        Research:
        {state["research_summary"]}
        """
    )

    return {
        "final_answer": response.content
    }


# --------------------------------------------------
# Main graph
# --------------------------------------------------

builder = StateGraph(MainState)

# Add reusable subgraph
builder.add_node(
    "research",
    research_graph
)

builder.add_node(
    "final_writer",
    final_writer
)


builder.add_edge(
    START,
    "research"
)

builder.add_edge(
    "research",
    "final_writer"
)

builder.add_edge(
    "final_writer",
    END
)


graph = builder.compile()


# --------------------------------------------------
# Run
# --------------------------------------------------

result = graph.invoke({
    "topic": "LangGraph persistence and human-in-the-loop",
})

print("\nFINAL ANSWER:")
print(result["final_answer"])
