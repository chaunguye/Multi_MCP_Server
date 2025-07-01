from fastmcp import FastMCP

mcp = FastMCP("user_retrieve")

@mcp.tool()
def get_user_info(userId):
    """
    This tool is used to get user name from user ID
    args:
        userId: string
    """
    return f"Get user info of {userId} is example data"

@mcp.tool()
def get_user_salary(userId):
    """
    This tool is used to get user salary from user ID
    args:
        userId: string
    """
    return f"Get user salary of {userId} is example data"

if __name__ == "__main__":
    mcp.run(transport="http")
