from registry import ToolRegistry
from router import Router
from transport import StdioTransport

from tools.calculator import CalculatorTool

registry = ToolRegistry()
registry.register_tool(CalculatorTool())
router = Router(registry)
transport = StdioTransport(router)
transport.start()
