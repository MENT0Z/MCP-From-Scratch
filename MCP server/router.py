from models import JsonRPCResponse

class Router:
    def __init__(self,registry):
        self.registry = registry

    def route(self,request):
        if request.method == "initialize":
            return JsonRPCResponse(
                id = request.id,
                result = {
                    "protocolVersion": "0.1",
                    "serverInfo": {
                        "name": "Scratch MCP",
                        "version": "1.0"
                    }

                }
            )
        
        elif request.method == "tools/list":
            return JsonRPCResponse(
                id=request.id,
                result={
                    "tools": self.registry.list_tools()
                }
            )
        
        elif request.method == "tools/call":
            tool = self.registry.get_tool(request.params["name"])
            output = tool.execute(request.params["arguments"])
            return JsonRPCResponse(
                id=request.id,
                result={
                    "output": output
                }
            )
        
        else:
            return JsonRPCResponse(
                id=request.id,
                error={
                    "code": -32601,
                    "message": "Method not found"
                }
            )