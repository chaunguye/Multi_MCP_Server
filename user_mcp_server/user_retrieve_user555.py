from fastmcp import FastMCP

user_retrieve_user555 = FastMCP("user_retrieve_user555")

@user_retrieve_user555.tool()
def get_user_info(userId):
    """
    This tool is used to get user name from user ID
    args:
        userId: string
    """
    return f"Get user info of {userId} is example data"

@user_retrieve_user555.tool()
def get_user_salary(userId):
    """
    This tool is used to get user salary from user ID
    args:
        userId: string
    """
    return f"Get user salary of {userId} is example data"

if __name__ == "__main__":
    user_retrieve_user555.run(transport="http")
