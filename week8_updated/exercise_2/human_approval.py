from typing import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import interrupt, Command

from common.llm import llm


class ApprovalState(TypedDict):
    request: str
    proposed_action: str
    approved: bool
    result: str


def analyze_request(state: ApprovalState):

    response = llm.invoke(
        f"""
        Analyze the following request:

        {state["request"]}

        Propose one concrete action that an AI system
        could perform.

        Do not execute the action.
        """
    )

    return {
        "proposed_action": response.content
    }


def human_approval(state: ApprovalState):

    decision = interrupt(
        {
            "message": "Human approval required",
            "request": state["request"],
            "proposed_action": state["proposed_action"],
        }
    )

    return {
        "approved": decision == "1"
    }


def execute_action(state: ApprovalState):

    if not state["approved"]:
        return {
            "result": "Action rejected by human."
        }

    response = llm.invoke(
        f"""
        Execute the following approved action conceptually:

        {state["proposed_action"]}

        Explain what would be done.
        """
    )

    return {
        "result": response.content
    }


def build_graph():

    builder = StateGraph(ApprovalState)

    builder.add_node("analyze", analyze_request)
    builder.add_node("human_approval", human_approval)
    builder.add_node("execute", execute_action)

    builder.add_edge(START, "analyze")
    builder.add_edge("analyze", "human_approval")
    builder.add_edge("human_approval", "execute")
    builder.add_edge("execute", END)

    checkpointer = InMemorySaver()

    return builder.compile(
        checkpointer=checkpointer
    )


def run():

    graph = build_graph()

    config = {
        "configurable": {
            "thread_id": "exercise-2"
        }
    }

    print("\n=== Exercise 2 ===")

    print("\nStarting workflow...")

    result = graph.invoke(
        {
            "request": "Delete the old customer database backup",
            "proposed_action": "",
            "approved": False,
            "result": "",
        },
        config=config
    )

    print("\nWorkflow interrupted.")
    print("Human approval is required.")

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

    print("\nType:")
    print("approve - 1")
    print("reject - 2")

    decision = input("\nYour decision: ").strip().lower()

    result = graph.invoke(
        Command(resume=decision),
        config=config
    )

    print("\nWorkflow completed.")
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
