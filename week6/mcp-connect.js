import { MultiServerMCPClient } from "@langchain/mcp-adapters";

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

  try {
    const tools = await client.getTools();

    console.log("\n===== MCP TOOLS =====\n");

    tools.forEach((tool, index) => {
      console.log(`${index + 1}. ${tool.name}`);
      console.log(`   ${tool.description}\n`);
    });

  } catch (err) {
    console.error(err);
  } finally {
    await client.close();
  }
}

main();