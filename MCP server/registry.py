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
    

class BaseTool:
    name = ""
    description = ""
    input_schema = {}

    def execute(self,arguments):
        raise NotImplementedError("Subclasses must implement the execute method.")
    
    def schema(self):
        return {
            "name": self.name,
            "description": self.description,
            "input_schema": self.input_schema
        }