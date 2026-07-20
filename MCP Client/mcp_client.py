import json 
import subprocess

class MCPClient:
    def __init__(self):
        self.process = subprocess.Popen(
            ["python", "../MCP server/main.py"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        self.id = 1

    def request(self,method,params=None):
        req = {
            "jsonrpc": "2.0",
            "id": self.id,
            "method": method,
            "params": params or {}
        }    

        self.id += 1
        self.process.stdin.write(json.dumps(req) + "\n")
        self.process.stdin.flush()

        response = self.process.stdout.readline()
        return json.loads(response)
    
    def initialize(self):
        return self.request("initialize")
    
    def list_tools(self):
        return self.request("tools/list")
    
    def call_tool(self,name,arguments):
        return self.request(
            "tools/call",
            {
                "name":name,
                "arguments":arguments
            }
        )