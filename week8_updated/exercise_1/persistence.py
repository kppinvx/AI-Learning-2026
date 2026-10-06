from typing import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver

from common.llm import llm


class WorkflowState(TypedDict):
    topic: str
    research: str
    summary: str


def research_node(state: WorkflowState):

    response = llm.invoke(
        f"""
        Research the following topic:

        {state["topic"]}

        Give me five important points.
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


def build_graph():

    builder = StateGraph(WorkflowState)

    builder.add_node("research", research_node)
    builder.add_node("summary", summary_node)

    builder.add_edge(START, "research")
    builder.add_edge("research", "summary")
    builder.add_edge("summary", END)

    checkpointer = InMemorySaver()

    return builder.compile(
        checkpointer=checkpointer
    )


def run():

    graph = build_graph()

    config = {
        "configurable": {
            "thread_id": "exercise-1"
        }
    }

    result = graph.invoke(
        {
            "topic": "Human-in-the-loop AI agents"
        },
        config=config
    )

    print("\n=== Exercise 1 ===")
    print("\nResearch:")
    # print(result["research"])
    if isinstance(result["research"], list):
        text = "".join(
            item.get("text", "")
            for item in result["research"]
            if item.get("type") == "text"
        )
    else:
        text = result["research"]
    print(f"\n{text}\n")

    print("\nSummary:")
    # print(result["summary"])
    if isinstance(result["summary"], list):
        text = "".join(
            item.get("text", "")
            for item in result["summary"]
            if item.get("type") == "text"
        )
    else:
        text = result["summary"]
    print(f"\n{text}\n")


if __name__ == "__main__":
    run()
