from fastmcp import FastMCP

user_retrieve_user459 = FastMCP("user_retrieve_user459")

@user_retrieve_user459.tool()
def get_user_salary(userId):
    """
    This tool is used to get user salary from user ID
    args:
        userId: string
    """
    return f"Get user salary of {userId} is example data"

if __name__ == "__main__":
    user_retrieve_user459.run(transport="http")
