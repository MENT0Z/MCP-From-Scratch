import asyncio
import json
from contextlib import AsyncExitStack

import requests

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


OLLAMA_URL = "http://localhost:11434/api/chat"
OLLAMA_MODEL = "llama3.1:latest"


with open("mcp_config.json") as f:
    config = json.load(f)


# --------------------------------
# MCP Globals
# --------------------------------

exit_stack = AsyncExitStack()

tool_to_session = {}
tools_for_llm = []


# --------------------------------
# Agent System Prompt
# --------------------------------

SYSTEM_PROMPT = """
You are an AI assistant with access to external tools.

Rules:

1. Only call tools when the user request requires it.
2. Do not call tools for greetings or casual conversation or normal question which doesnt requires external tools.
3. If no tool is needed, answer the user normally for their question and dont mention like i will not call tools , just give them answer for that question.
3. Before calling a tool, decide whether it is actually necessary.
4. After receiving tool results, explain the result clearly.
5. Never explain how to manually perform an action if a tool already did it.
"""


# --------------------------------
# Ollama
# --------------------------------

def chat(messages, tools=None):

    payload = {
        "model": OLLAMA_MODEL,
        "messages": messages,
        "stream": False
    }

    if tools:
        payload["tools"] = tools


    response = requests.post(
        OLLAMA_URL,
        json=payload
    )

    response.raise_for_status()

    return response.json()



# --------------------------------
# Connect MCP Servers
# --------------------------------

async def connect_servers():

    for server_name, server in config["mcpServers"].items():

        print(f"\nConnecting to {server_name}...")


        params = StdioServerParameters(
            command=server["command"],
            args=server["args"],
            env=server.get("env")
        )


        read_stream, write_stream = await exit_stack.enter_async_context(
            stdio_client(params)
        )


        session = await exit_stack.enter_async_context(
            ClientSession(
                read_stream,
                write_stream
            )
        )


        await session.initialize()


        result = await session.list_tools()


        for tool in result.tools:

            print("   ", tool.name)


            tool_to_session[tool.name] = session


            tools_for_llm.append(
                {
                    "type": "function",
                    "function":
                    {
                        "name": tool.name,
                        "description": tool.description,
                        "parameters": tool.inputSchema
                    }
                }
            )



# --------------------------------
# Execute MCP Tool
# --------------------------------

async def execute_tool(
        tool_name,
        arguments
):

    session = tool_to_session.get(tool_name)


    if session is None:
        raise Exception(
            f"Tool not found: {tool_name}"
        )


    result = await session.call_tool(
        tool_name,
        arguments
    )


    return result.content



# --------------------------------
# Main Agent Loop
# --------------------------------

async def main():


    await connect_servers()


    conversation = [
        {
            "role":"system",
            "content":SYSTEM_PROMPT
        }
    ]


    while True:


        prompt = input("\nYou: ")


        if prompt.lower() in [
            "exit",
            "quit"
        ]:
            break



        conversation.append(
            {
                "role":"user",
                "content":prompt
            }
        )



        # First LLM call
        response = chat(
            conversation,
            tools=tools_for_llm
        )


        msg = response["message"]



        # No tool call
        if "tool_calls" not in msg:


            print(
                "\nAI:",
                msg["content"]
            )


            conversation.append(msg)

            continue



        # Add assistant tool request
        conversation.append(msg)



        # Execute all requested tools

        for call in msg["tool_calls"]:


            tool_name = call["function"]["name"]


            arguments = call["function"]["arguments"]


            if isinstance(arguments, str):
                arguments = json.loads(arguments)



            print(
                f"\nCalling tool: {tool_name}"
            )

            print(
                arguments
            )


            result = await execute_tool(
                tool_name,
                arguments
            )



            conversation.append(
                {
                    "role":"tool",
                    "content":json.dumps(
                        result,
                        default=str
                    )
                }
            )



        # Second LLM call
        final = chat(
            conversation
        )


        final_msg = final["message"]


        print(
            "\nAI:",
            final_msg["content"]
        )


        conversation.append(final_msg)



if __name__ == "__main__":

    asyncio.run(main())