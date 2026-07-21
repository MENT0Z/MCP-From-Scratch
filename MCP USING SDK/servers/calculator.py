from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Calculator Server")

# here in the fast mcp whatever we wrote in the comment goes in the description field

@mcp.tool()
def add(a:int,b:int)->int:
    """
    tool that is used to add two numbers
    """
    return a+b

@mcp.tool()
def multiply(a:int,b:int)->int:
    """
    tool that is used to multiply two numbers
    """
    return a*b

if __name__ == "__main__":
    mcp.run()