import { ChatGoogleGenerativeAI } from "@langchain/google-genai";
import { createAgent } from "langchain";
import { MultiServerMCPClient } from "@langchain/mcp-adapters";

process.env.GOOGLE_API_KEY = "YOUR_GEMINI_API_KEY";

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
        "@modelcontextprotocol/server-sqlite",
        "./sample.db"
      ]
    }
  });

  const tools = await client.getTools();

  const llm = new ChatGoogleGenerativeAI({
    model: "gemini-2.5-flash",
    temperature: 0
  });

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

// import { ChatMistralAI } from "@langchain/mistralai";

// const llm = new ChatMistralAI({
//   apiKey: process.env.MISTRAL_API_KEY,
//   model: "mistral-small-latest",
//   temperature: 0
// });
