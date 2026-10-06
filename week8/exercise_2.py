from typing import TypedDict

from langchain_google_genai import ChatGoogleGenerativeAI

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import interrupt, Command
from dotenv import load_dotenv

load_dotenv()


# --------------------------------------------------
# State
# --------------------------------------------------

class ApprovalState(TypedDict):
    request: str
    proposed_action: str
    approved: bool
    result: str


# --------------------------------------------------
# Gemini
# --------------------------------------------------

llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    temperature=0
)


# --------------------------------------------------
# Step 1: Gemini proposes an action
# --------------------------------------------------

def analyze_request(state: ApprovalState):

    response = llm.invoke(
        f"""
        Analyze this request:

        {state["request"]}

        Propose one concrete action that an AI system
        could perform to satisfy the request.

        Do not execute anything.
        """
    )

    return {
        "proposed_action": response.content
    }


# --------------------------------------------------
# Step 2: Human approval
# --------------------------------------------------

def human_approval(state: ApprovalState):

    decision = interrupt({
        "type": "approval_request",
        "message": "Human approval required",
        "request": state["request"],
        "proposed_action": state["proposed_action"]
    })

    return {
        "approved": decision == "approve"
    }


# --------------------------------------------------
# Step 3: Execute action
# --------------------------------------------------

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


# --------------------------------------------------
# Build graph
# --------------------------------------------------

builder = StateGraph(ApprovalState)

builder.add_node("analyze", analyze_request)
builder.add_node("human_approval", human_approval)
builder.add_node("execute", execute_action)

builder.add_edge(START, "analyze")
builder.add_edge("analyze", "human_approval")
builder.add_edge("human_approval", "execute")
builder.add_edge("execute", END)


# --------------------------------------------------
# Checkpointer
# --------------------------------------------------

checkpointer = InMemorySaver()

graph = builder.compile(
    checkpointer=checkpointer
)


# --------------------------------------------------
# Thread
# --------------------------------------------------

config = {
    "configurable": {
        "thread_id": "approval-001"
    }
}


# --------------------------------------------------
# Initial execution
# --------------------------------------------------

print("\nStarting workflow...")

result = graph.invoke(
    {
        "request": "Delete the old customer database backup",
        "approved": False,
        "result": ""
    },
    config=config
)

print("\nWorkflow paused.")
print(result)
