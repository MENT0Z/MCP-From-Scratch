class ToolRegistry:
    def __init__(self):
        self.tools = {}
    
    def register_tool(self,tool):
        self.tools[tool.name] = tool
    
    def get_tool(self,name):
        return self.tools[name]
    
    def list_tools(self):
        return [
            tool.schema() for tool in self.tools.values()
        ]