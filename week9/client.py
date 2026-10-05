import asyncio
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from fastmcp import Client


load_dotenv()

MCP_SERVER_URL = "http://localhost:8000/mcp"


async def main():

    # --------------------------------------------------
    # 1. Connect to MCP server
    # --------------------------------------------------

    async with Client(MCP_SERVER_URL) as mcp_client:

        # --------------------------------------------------
        # 2. Discover MCP tools
        # --------------------------------------------------

        mcp_tools = await mcp_client.list_tools()

        print("\nAvailable MCP tools:\n")

        for tool in mcp_tools:
            print(f"- {tool.name}")
            print(f"  {tool.description}")
            print()

        # --------------------------------------------------
        # 3. Convert MCP tools to Gemini function declarations
        # --------------------------------------------------

        function_declarations = []

        for tool in mcp_tools:

            function_declarations.append(
                types.FunctionDeclaration(
                    name=tool.name,
                    description=tool.description,
                    parameters_json_schema=tool.input_schema,
                )
            )

        gemini_tools = [
            types.Tool(
                function_declarations=function_declarations
            )
        ]

        # --------------------------------------------------
        # 4. Create Gemini client
        # --------------------------------------------------

        gemini = genai.Client(
            api_key=os.environ["GOOGLE_API_KEY"]
        )

        user_question = (
            "Find employees who have AWS skills. "
            "Tell me their names, roles and locations."
        )

        print("\nUser:")
        print(user_question)

        # --------------------------------------------------
        # 5. Maintain conversation history
        # --------------------------------------------------

        contents = [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(
                        text=user_question
                    )
                ],
            )
        ]

        # --------------------------------------------------
        # 6. First Gemini request
        # --------------------------------------------------

        response = gemini.models.generate_content(
            model="gemini-3.6-flash",
            contents=contents,
            config=types.GenerateContentConfig(
                tools=gemini_tools,
            ),
        )

        # --------------------------------------------------
        # 7. Add Gemini's response to conversation
        # --------------------------------------------------

        contents.append(response.candidates[0].content)

        # --------------------------------------------------
        # 8. Check for function calls
        # --------------------------------------------------

        function_response_parts = []

        for part in response.candidates[0].content.parts:

            if part.function_call is None:
                continue

            function_call = part.function_call

            print("\nGemini wants to call:")
            print(function_call.name)

            print("\nArguments:")
            print(function_call.args)

            # --------------------------------------------------
            # 9. Execute MCP tool
            # --------------------------------------------------

            mcp_result = await mcp_client.call_tool(
                function_call.name,
                function_call.args,
            )

            print("\nMCP result:")
            print(mcp_result.data)

            # --------------------------------------------------
            # 10. Convert MCP result into Gemini
            #     function response
            # --------------------------------------------------

            function_response_parts.append(
                types.Part.from_function_response(
                    name=function_call.name,
                    response={
                        "result": mcp_result.data
                    },
                )
            )

        # --------------------------------------------------
        # 11. Add function response to conversation
        # --------------------------------------------------

        if function_response_parts:

            contents.append(
                types.Content(
                    role="user",
                    parts=function_response_parts,
                )
            )

        # --------------------------------------------------
        # 12. Ask Gemini to generate final answer
        # --------------------------------------------------

        final_response = gemini.models.generate_content(
            model="gemini-3.6-flash",
            contents=contents,
            config=types.GenerateContentConfig(
                tools=gemini_tools,
            ),
        )

        print("\nGemini final answer:")
        print(final_response.text)


if __name__ == "__main__":
    asyncio.run(main())