from ollama_client import OllamaClient
from mcp_client import MCPClient
from parser import parse_tool_call
from prompts import SYSTEM_PROMPT
import json


class Agent:
    def __init__(self):
        self.llm = OllamaClient()
        self.mcp = MCPClient()
        self.mcp.initialize()

    def chat(self, user_message):
        tools = self.mcp.list_tools()["result"]["tools"]
        tool_text = json.dumps(
            tools,
            indent=2
        )
        messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
                + "\n\nAvailable tools:\n"
                + tool_text
            },
            {
                "role": "user",
                "content": user_message
            }
        ]
        answer = self.llm.chat(messages)
        tool = parse_tool_call(answer)

        if tool is None:
            return answer

        tool_result = self.mcp.call_tool(
            tool["tool"],
            tool["arguments"]
        )

        final = self.llm.chat(
            [
                {
                    "role": "system",
                    "content": "Answer using tool result."
                },
                {
                    "role": "user",
                    "content": user_message
                },
                {
                    "role": "assistant",
                    "content": str(tool)
                },
                {
                    "role": "tool",
                    "content": str(tool_result["result"])
                }
            ]
        )
        return final