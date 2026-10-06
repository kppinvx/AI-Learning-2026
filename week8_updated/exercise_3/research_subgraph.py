from typing import TypedDict

from langgraph.graph import StateGraph, START, END

from common.llm import llm


class ResearchState(TypedDict):
    topic: str
    research: str
    critique: str
    research_summary: str


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


def critic(state: ResearchState):

    response = llm.invoke(
        f"""
        You are a research critic.

        Review this research:

        {state["research"]}

        Identify:
        - missing information
        - questionable claims
        - areas needing clarification
        """
    )

    return {
        "critique": response.content
    }


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


def build_research_subgraph():

    builder = StateGraph(ResearchState)

    builder.add_node("researcher", researcher)
    builder.add_node("critic", critic)
    builder.add_node("summarizer", summarize_research)

    builder.add_edge(START, "researcher")
    builder.add_edge("researcher", "critic")
    builder.add_edge("critic", "summarizer")
    builder.add_edge("summarizer", END)

    return builder.compile()
