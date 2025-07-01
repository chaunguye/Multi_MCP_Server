
import asyncio
from fastmcp import Client


class ToolFormat:
    def __init__(self, name, descrip, input_schema):
        self.name = name
        self.description = descrip
        self.input_schema = input_schema


class SimpleChatBot:
    def __init__(self):
        self.session = None
        self.available_tools: List[ToolFormat] = []
        self.serverURL = "http://127.0.0.1:8000"

    async def connect_to_server(self):
        """This is the function for Client to connect to Server"""
        try:
            session = Client("http://127.0.0.1:8000/mcp-user301/mcp")
            ## This is the address of FastAPI Server http://127.0.0.1:8000 and the /mcp-user891/mcp
            ## is the mcp server of user 891 mounted to FastAPI Server
            self.session = session
            async with self.session:
                response_tools = await session.list_tools()
                print(f"Available tools: {response_tools}")
                print(f"\nConnected to {self.serverURL} with tools:", [t.name for t in response_tools])
        except Exception as e:
            print(f"Failed to connect to {self.serverURL}: {e}")

    async def test_call_tool(self):
        async with self.session:
            param_test = {
                "userId": "1234"
            }
            result = await self.session.call_tool("get_user_info",param_test)
            print(result)



async def main():
    chatbot = SimpleChatBot()
 
    await chatbot.connect_to_server() 
    # await chatbot.test_call_tool() 
    

if __name__ == "__main__":
    asyncio.run(main())


        
            