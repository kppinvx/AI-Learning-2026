A useful mental model is:

- LLM = brain
- Tools = hands
- Agent = brain + hands + decision-making loop

## When is an Agent Appropriate?

Not every LLM application needs an agent.
If you only need:

User → LLM → Answer

Example:

"Explain what Redis is."

No agent is necessary.

Use an agent when the LLM needs to determine which tools to use and in what order:

For example:

"Find my last completed appointment and tell me how much I paid."

The agent may need to:

1. Search appointments.
2. Identify the completed appointment.
3. Retrieve payment information.
4. Calculate/display the amount.
5. Answer the user.

The exact sequence can be decided dynamically by the LLM.


A tool generally has:

- name
- description
- input schema
- function implementation

## LangChain Default Tools

LangChain provides many pre-built integrations/tools, so you don't always have to implement everything yourself.

Examples include tools for things such as:

- search
- HTTP requests
- SQL databases
- vector stores
- calculators
- file operations
- APIs
- code execution
- various third-party services

## Agent vs Tool Calling

These terms are related but not identical.
Tool calling The LLM decides: "I need this tool."

The important idea is that the agent observes the result of one action before deciding what to do next.

## ReAct in a Real Application

Imagine your healthcare application has:
- search_patient
- get_appointments
- get_doctor
- get_payment

User:

"What doctor did I see in my last completed appointment and how much did I pay?"

The agent could do:

                    User
                      │
                      ▼
                    Agent
                      │
              ┌───────┴────────┐
              ▼                │
       search_patient          │
              │                │
              ▼                │
        Patient ID             │
              │                │
              ▼                │
       get_appointments        │
              │                │
              ▼                │
       Completed appointment   │
              │                │
              ▼                │
          get_doctor           │
              │                │
              ▼                │
        Doctor information     │
              │                │
              ▼                │
          get_payment          │
              │                │
              ▼                │
         Payment amount        │
              │                │
              └───────┬────────┘
                      ▼
                 Final answer

This is a good agent use case because the required operations depend on the results of previous operations.

## A Simple LangChain Architecture

                    ┌───────────────┐
                    │     User      │
                    └───────┬───────┘
                            │
                            ▼
                    ┌───────────────┐
                    │     Agent     │
                    │               │
                    │      LLM      │
                    └───────┬───────┘
                            │
              ┌─────────────┼─────────────┐
              │             │             │
              ▼             ▼             ▼
        ┌──────────┐  ┌──────────┐  ┌──────────┐
        │ DB Tool  │  │ API Tool │  │ Search   │
        └────┬─────┘  └────┬─────┘  └────┬─────┘
             │             │             │
             ▼             ▼             ▼
          MySQL        REST API      Search API

Your tools become the controlled interface between the LLM and your infrastructure.

## When NOT to Use an Agent

This is very important.

Don't use an agent just because you're building an AI application.

For example:

User asks:
"Show my appointments."

You probably don't need an agent.

A deterministic workflow is better:

User → API → Database → Response

Likewise:

User asks:
"Summarize this document."

You probably don't need an agent.

A straightforward RAG/document-processing pipeline may be sufficient.

Agents add:

- latency
- token consumption
- complexity
- nondeterminism
- additional security concerns
- debugging difficulty

## Good Agent Use Cases

Agents are particularly useful when there are:
Multiple possible tools

- Search
- Database
- CRM
- Email
- Calendar
- Payment
- Analytics

Dynamic workflows

For example:

"Find customers who haven't paid, check their recent orders, and draft a follow-up."

Multi-step tasks
Search → Analyze → Calculate → Update

Ambiguous natural-language requests

For example:

"Move my appointment to the earliest available slot next week."

The agent might need:

get_current_appointment() → get_available_slots() → select suitable slot → update_appointment()

## Agent Architecture in One Picture

                         ┌──────────────┐
                         │     User     │
                         └──────┬───────┘
                                │
                                ▼
                     ┌────────────────────┐
                     │       Agent        │
                     │                    │
                     │  LLM + Instructions│
                     └─────────┬──────────┘
                               │
                    "What should I do?"
                               │
             ┌─────────────────┼──────────────────┐
             │                 │                  │
             ▼                 ▼                  ▼
        ┌─────────┐       ┌─────────┐       ┌──────────┐
        │ Tool 1  │       │ Tool 2  │       │ Tool 3   │
        │ Search  │       │   DB    │       │   API    │
        └────┬────┘       └────┬────┘       └────┬─────┘
             │                 │                  │
             └─────────────────┼──────────────────┘
                               │
                               ▼
                         Tool results
                               │
                               ▼
                           Agent/LLM
                               │
                       "What next?"
                               │
                         ┌─────┴─────┐
                         │           │
                       Tool       Final answer

And the relationship is:

    LangChain tools
        │
        ├── Default tools
        │
        └── Custom tools
                │
                ▼
            Tool calling
                │
                ▼
            Agent
                │
                ▼
            ReAct
        Reason → Act → Observe
                ↺


## The key takeaway

- Tools are the capabilities.
- Tool calling is how the LLM requests those capabilities.
- An agent is the decision-making system that chooses and sequences those capabilities.
- ReAct is one classic pattern for implementing that iterative decision/action process.
