import asyncio
import json

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# -------------------------
# Load MCP servers
# -------------------------

with open("mcp_config.json") as f:
    config=json.load(f)



sessions=[]



async def connect_servers():

    tools=[]


    for name,server in config["mcpServers"].items():

        params=StdioServerParameters(
            command=server["command"],
            args=server["args"],
            env=server.get("env")
        )


        transport = await stdio_client(params).__aenter__()

        session = ClientSession(
            transport[0],
            transport[1]
        )

        await session.initialize()


        sessions.append(
            {
            "name":name,
            "session":session
            }
        )


        result = await session.list_tools()


        for t in result.tools:

            tools.append(
                {
                "type":"function",
                "function":{
                    "name":t.name,
                    "description":t.description,
                    "parameters":t.inputSchema
                }
                }
            )


    return tools



# -------------------------
# Tool executor
# -------------------------


async def execute_tool(name,args):


    for server in sessions:

        session=server["session"]

        tools=await session.list_tools()


        for tool in tools.tools:

            if tool.name==name:

                result=await session.call_tool(
                    name,
                    args
                )

                return result.content



# -------------------------
# Chat loop
# -------------------------
import requests
OLLAMA_URL = "http://localhost:11434/api/chat"
OLLAMA_MODEL = "gemma3:latest"
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



async def main():
    tools=await connect_servers()

    while True:


        prompt=input("\nYou: ")

        # use above chat fun
        response = chat(
            [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            tools=tools
        )


        msg=response["message"]



        if msg.get("tool_calls"):


            for call in msg["tool_calls"]:


                name=call["function"]["name"]

                args=call["function"]["arguments"]


                result=await execute_tool(
                    name,
                    args
                )


                final = chat(
                    [
                        {
                            "role": "user",
                            "content": prompt
                        },
                        msg,
                        {
                            "role": "tool",
                            "content": str(result)
                        }
                    ]
                )


                print(
                    "\nAI:",
                    final["message"]["content"]
                )


        else:

            print(
                "\nAI:",
                msg["content"]
            )



asyncio.run(main())