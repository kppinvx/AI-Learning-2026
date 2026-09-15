import { ChatGoogleGenerativeAI } from "@langchain/google-genai";
import { ChatMistralAI } from "@langchain/mistralai";
import { createAgent } from "langchain";
import { MultiServerMCPClient } from "@langchain/mcp-adapters";
import dotenv from 'dotenv';
dotenv.config();

async function main() {

  const client = new MultiServerMCPClient({
    filesystem: {
      transport: "stdio",
      command: "npx",
      args: [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "./"
      ]
    },

    sqlite: {
      transport: "stdio",
      command: "npx",
      args: [
        "-y",
        "@modelcontextprotocol/server-memory"
      ]
    }
  });

  const tools = await client.getTools();

  const llm = new ChatGoogleGenerativeAI({
    apiKey: process.env.GOOGLE_API_KEY,
    model: "gemini-3.6-flash",
    temperature: 0
  });

  // const llm = new ChatMistralAI({
  //   apiKey: process.env.MISTRAL_API_KEY,
  //   model: "mistral-small-latest",
  //   temperature: 0
  // });

  const agent = createAgent({
    model: llm,
    tools
  });

  const response = await agent.invoke({
    messages: [
      {
        role: "user",
        content:
          "List files from current directory and tell me whether any sql database exists."
      }
    ]
  });

  console.log(response.messages.at(-1)?.content);

  await client.close();
}

main();
