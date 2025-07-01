from fastmcp import FastMCP

mcp891 = FastMCP("user_retrieve_user891")

@mcp891.tool()
def get_user_salary(userId):
    """
    This tool is used to get user salary from user ID
    args:
        userId: string
    """
    return f"Get user salary of {userId} is example data"



if __name__ == "__main__":
    mcp891.run(transport="http",
            host="127.0.0.1",
            port=4200,)
