from fastmcp import FastMCP

user_retrieve_user119 = FastMCP("user_retrieve_user119")

@user_retrieve_user119.tool()
def get_user_info(userId):
    """
    This tool is used to get user name from user ID
    args:
        userId: string
    """
    return f"Get user info of {userId} is example data"



if __name__ == "__main__":
    user_retrieve_user119.run(transport="http")
