from fastmcp import FastMCP

mcp301 = FastMCP("user_retrieve")

@mcp301.tool()
def get_user_info(userId):
    """
    This tool is used to get user name from user ID
    args:
        userId: string
    """
    return f"Get user info of {userId} is example data"

@mcp301.tool()
def get_user_salary(userId):
    """
    This tool is used to get user salary from user ID
    args:
        userId: string
    """
    return f"Get user salary of {userId} is example data"

if __name__ == "__main__":
    mcp301.run(transport="http",
            host="127.0.0.1",
            port=4202,)
