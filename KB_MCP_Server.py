from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Knowledge Base Retrieve")

@mcp.tool()
def get_user_info(userId):
    """
    This tool is used to retrieve user's information based-on user ID
    args:
        userId: User ID used to retrieve information
    """
    return f"Name of {str(userId)} is Nguyen Van A"

@mcp.tool()
def get_user_salary(userId):
    """
    This tool is used to retrieve user's salary based-on user ID
    args:
        userId: User ID used to retrieve salary
    """
    return f"Salary of {str(userId)} is 1,000,000"



@mcp.resource("mcp://knowledge_base/{kbId}")
def search_knowledge_base(kbId):
    """This resource is exposing knowledge base based-on knowledge base ID
    kbId: the ID of knowledge base to retrieve"""
    return f"This is the knowledge base id {kbId} for the chatbot MoGenie"

@mcp.resource("mcp://knowledge_base")
def search_knowledge_base():
    """This resource is exposing knowledge base based-on knowledge base ID
    kbId: the ID of knowledge base to retrieve"""
    return "This is the knowledge base id for the chatbot MoGenie"

if __name__ == "__main__":
    mcp.run(transport="sse")