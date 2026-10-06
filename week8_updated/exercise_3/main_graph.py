from typing import TypedDict

from langgraph.graph import StateGraph, START, END

from common.llm import llm
from exercise_3.research_subgraph import build_research_subgraph


class MainState(TypedDict):
    topic: str
    research_summary: str
    final_answer: str


research_graph = build_research_subgraph()


def final_writer(state: MainState):

    response = llm.invoke(
        f"""
        You are a senior technical writer.

        Create a clear final answer based on this research.

        Topic:
        {state["topic"]}

        Research:
        {state["research_summary"]}
        """
    )

    return {
        "final_answer": response.content
    }


def build_graph():

    builder = StateGraph(MainState)

    # Reusable subgraph
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

    return builder.compile()


def run():

    graph = build_graph()

    result = graph.invoke(
        {
            "topic": "LangGraph persistence and human-in-the-loop",
            "research_summary": "",
            "final_answer": "",
        }
    )

    print("\n=== Exercise 3 ===")

    print("\nFinal answer:")
    # print(result["final_answer"])
    if isinstance(result["final_answer"], list):
        text = "".join(
            item.get("text", "")
            for item in result["final_answer"]
            if item.get("type") == "text"
        )
    else:
        text = result["final_answer"]
    print(f"\n{text}\n")


if __name__ == "__main__":
    run()
