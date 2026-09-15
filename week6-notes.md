## LangChain + MCP (Model Context Protocol)

MCP is a standard protocol that allows external applications and services to expose tools, prompts, resources, and data to LLMs. LangChain can connect to MCP servers and automatically convert MCP tools into LangChain tools.

## The langchain-mcp-adapters Library

The adapter library acts as a bridge between MCP servers and LangChain.

Main capabilities:
- Connect to one or more MCP servers
- Load MCP tools as LangChain tools
- Use MCP tools inside agents
- Support stdio, HTTP, SSE transports
- Support prompts, resources, and structured tool output

## Connecting to MCP Servers

1. stdio Transport (Local MCP Server)
Use when:

- Local tools
- Local databases
- Development/testing
- Desktop applications

stdio is commonly used with open-source MCP servers running on your machine.

