import "dotenv/config";

import { StateGraph, START, END } from "@langchain/langgraph";
import { ChatGoogleGenerativeAI } from "@langchain/google-genai";
import { z } from "zod";

const llm = new ChatGoogleGenerativeAI({
  model: "gemini-3.6-flash",
  temperature: 0,
});

// State
const GraphState = z.object({
  question: z.string(),
  plan: z.string().optional(),
  retrievedDocs: z.array(z.string()).default([]),
  summary: z.string().optional(),
  finalAnswer: z.string().optional(),
});

// Planning Agent
async function planningAgent(state) {
  const response = await llm.invoke(`
You are a research planner.

Question:
${state.question}

Create a research plan with:
1. Topics to investigate
2. Important facts needed
3. Search queries to run

Return concise output.
`);

  return {
    plan: response.content,
  };
}

// Retrieval Agent
async function retrievalAgent(state) {
  const response = await llm.invoke(`
You are simulating a retrieval system.

Research Plan:
${state.plan}

Question:
${state.question}

Generate 5 research notes that would likely be
retrieved from trusted sources.
`);

  return {
    retrievedDocs: [response.content],
  };
}

// Summarization Agent
async function summarizationAgent(state) {
  const docs = state.retrievedDocs.join("\n\n");

  const response = await llm.invoke(`
You are a research summarizer.

Research Material:
${docs}

Create a concise factual summary.
`);

  return {
    summary: response.content,
  };
}

// Final Answer Agent
async function finalAnswerAgent(state) {
  const response = await llm.invoke(`
Question:
${state.question}

Research Summary:
${state.summary}

Generate a detailed final answer.
`);

  return {
    finalAnswer: response.content,
  };
}

// Build Graph
const graph = new StateGraph(GraphState)
  .addNode("planner", planningAgent)
  .addNode("retriever", retrievalAgent)
  .addNode("summarizer", summarizationAgent)
  .addNode("answerGenerator", finalAnswerAgent)
  .addEdge(START, "planner")
  .addEdge("planner", "retriever")
  .addEdge("retriever", "summarizer")
  .addEdge("summarizer", "answerGenerator")
  .addEdge("answerGenerator", END);

const app = graph.compile();

// Run
const result = await app.invoke({
  question: "Explain how MCP servers work and compare them with REST APIs",
});

console.log("\n========== PLAN ==========\n");
console.log(result.plan);

console.log("\n========== SUMMARY ==========\n");
console.log(result.summary);

console.log("\n========== FINAL ANSWER ==========\n");
console.log(result.finalAnswer);
