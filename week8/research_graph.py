from typing import TypedDict

from langchain_google_genai import ChatGoogleGenerativeAI

from langgraph.graph import StateGraph, START, END

from dotenv import load_dotenv

load_dotenv()


# --------------------------------------------------
# State for the subgraph
# --------------------------------------------------

class ResearchState(TypedDict):
    topic: str
    research: str
    critique: str
    research_summary: str


llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    temperature=0
)


# --------------------------------------------------
# Research agent
# --------------------------------------------------

def researcher(state: ResearchState):

    response = llm.invoke(
        f"""
        You are a research agent.

        Research this topic:

        {state["topic"]}

        Provide useful technical information.
        """
    )

    return {
        "research": response.content
    }


# --------------------------------------------------
# Critic agent
# --------------------------------------------------

def critic(state: ResearchState):

    response = llm.invoke(
        f"""
        You are a research critic.

        Review the following research:

        {state["research"]}

        Identify:
        - missing information
        - questionable claims
        - areas that need clarification
        """
    )

    return {
        "critique": response.content
    }


# --------------------------------------------------
# Research summarizer
# --------------------------------------------------

def summarize_research(state: ResearchState):

    response = llm.invoke(
        f"""
        Create a concise research summary.

        Research:
        {state["research"]}

        Critique:
        {state["critique"]}
        """
    )

    return {
        "research_summary": response.content
    }


# --------------------------------------------------
# Build subgraph
# --------------------------------------------------

builder = StateGraph(ResearchState)

builder.add_node("researcher", researcher)
builder.add_node("critic", critic)
builder.add_node("summarizer", summarize_research)

builder.add_edge(START, "researcher")
builder.add_edge("researcher", "critic")
builder.add_edge("critic", "summarizer")
builder.add_edge("summarizer", END)

research_graph = builder.compile()
