from typing import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import interrupt, Command

from common.llm import llm
from exercise_3.research_subgraph import build_research_subgraph


# ==================================================
# State
# ==================================================

class MainState(TypedDict):
    topic: str
    research_summary: str
    proposed_action: str
    approved: bool
    result: str


# ==================================================
# Reusable research subgraph
# ==================================================

research_graph = build_research_subgraph()


# ==================================================
# Proposal node
# ==================================================

def create_proposal(state: MainState):

    response = llm.invoke(
        f"""
        Based on the research below, propose one
        important action that an AI system could perform.

        Topic:
        {state["topic"]}

        Research:
        {state["research_summary"]}

        Do not execute the action.
        """
    )

    return {
        "proposed_action": response.content
    }


# ==================================================
# Human approval
# ==================================================

def human_approval(state: MainState):

    decision = interrupt(
        {
            "message": "Human approval required",
            "topic": state["topic"],
            "proposed_action": state["proposed_action"],
        }
    )

    return {
        "approved": decision == "1"
    }


# ==================================================
# Execute action
# ==================================================

def execute_action(state: MainState):

    if not state["approved"]:

        return {
            "result": "Action rejected by human."
        }

    response = llm.invoke(
        f"""
        Execute the following approved action conceptually:

        {state["proposed_action"]}

        Explain the result.
        """
    )

    return {
        "result": response.content
    }


# ==================================================
# Build graph
# ==================================================

def build_graph():

    builder = StateGraph(MainState)

    builder.add_node(
        "research",
        research_graph
    )

    builder.add_node(
        "create_proposal",
        create_proposal
    )

    builder.add_node(
        "human_approval",
        human_approval
    )

    builder.add_node(
        "execute",
        execute_action
    )

    builder.add_edge(
        START,
        "research"
    )

    builder.add_edge(
        "research",
        "create_proposal"
    )

    builder.add_edge(
        "create_proposal",
        "human_approval"
    )

    builder.add_edge(
        "human_approval",
        "execute"
    )

    builder.add_edge(
        "execute",
        END
    )

    checkpointer = InMemorySaver()

    return builder.compile(
        checkpointer=checkpointer
    )


# ==================================================
# Run
# ==================================================

def run():

    graph = build_graph()

    config = {
        "configurable": {
            "thread_id": "combined-workflow-001"
        }
    }

    print("\n======================================")
    print("LangGraph Combined Exercise")
    print("======================================")

    print("\nStarting workflow...")

    result = graph.invoke(
        {
            "topic": "Human-in-the-loop AI agents",
            "research_summary": "",
            "proposed_action": "",
            "approved": False,
            "result": "",
        },
        config=config
    )

    print("\n======================================")
    print("Workflow paused")
    print("======================================")

    print("\nProposed action:")
    # print(result["proposed_action"])
    if isinstance(result["proposed_action"], list):
        text = "".join(
            item.get("text", "")
            for item in result["proposed_action"]
            if item.get("type") == "text"
        )
    else:
        text = result["proposed_action"]
    print(f"\n{text}\n")

    decision = input(
        "\nApprove this action? "
        "(approve - 1/reject - 2): "
    ).strip().lower()

    result = graph.invoke(
        Command(resume=decision),
        config=config
    )

    print("\n======================================")
    print("Workflow completed")
    print("======================================")

    # print(result["result"])
    if isinstance(result["result"], list):
        text = "".join(
            item.get("text", "")
            for item in result["result"]
            if item.get("type") == "text"
        )
    else:
        text = result["result"]
    print(f"\n{text}\n")


if __name__ == "__main__":
    run()
