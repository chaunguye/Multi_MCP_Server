from mcp.client.sse import sse_client
from contextlib import AsyncExitStack
import anthropic
from typing import List, Dict
from mcp import ClientSession
import asyncio
from dotenv import load_dotenv
import os
import openai
import json
from google import genai
from google.genai import types
from fastmcp import Client

api_key = os.getenv("api_key")
client = genai.Client(api_key)
model = "gemini-2.0-flash-live-001"

class ToolFormat:
    def __init__(self, name, descrip, input_schema):
        self.name = name
        self.description = descrip
        self.input_schema = input_schema


class SimpleChatBot:
    def __init__(self):
        self.session = None
        self.exit_stack = AsyncExitStack() # new
        # self.anthropic = anthropic.Anthropic()
        self.available_tools: List[ToolFormat] = []
        self.serverURL = "http://127.0.0.1:8000" 

    async def connect_to_server(self):
        """This is the function for Client to connect to Server"""
        try:
            # sse_transport = await self.exit_stack.enter_async_context(
            #             sse_client(url= f"{self.serverURL}/mcp" )
            #             )
            # read, write = sse_transport 
            # session = await self.exit_stack.enter_async_context(
            #         ClientSession(read, write)
            #     )
            session = Client("https://127.0.0.1:8000/mcp")
            # await session.initialize()
            self.session = session
            async with client:
                response_tools = await session.list_tools()
                # print(tools)
                
                tools = response_tools.tools
                print(f"\nConnected to {self.serverURL} with tools:", [t.name for t in tools])
                self.available_tools = [ToolFormat(tool.name, tool.description, tool.inputSchema) for tool in tools]
            # print(self.available_tools)
        except Exception as e:
            print(f"Failed to connect to {self.serverURL}: {e}")

    async def get_resource(self, kbid):
        # result_session = self.session.get(f"knowledge_base://{kbid}")

        # if not result_session:
        #     print(f"No result found for knowledge base {kbid}")
        # else:

        uri_ne = f"mcp://knowledge_base/{kbid}"
        try:
            content = await self.session.read_resource(uri=uri_ne)
            print("Content: ", content.contents[0].text)
        except Exception as e:
            print(f"Can connect to URI: {uri_ne} because {e}")


    async def simple_chat(self, query):

        tools = [
                {
                    "function_declarations": [{
                        "name": tool.name,
                        "description": tool.description,
                        "parameters": {
                            "type": "object",
                            # "properties": tool.input_schema.get("properties", {}),
                            "properties": tool.input_schema.get("properties", {}),
                            "required": tool.input_schema.get("required", [])
                        }
                    }
                    for tool in self.available_tools
                    ]
                }
            ] 
        print(tools)


        config = {"response_modalities": ["TEXT"], "tools": tools}

        async with client.aio.live.connect(model=model, config=config) as gemi_session:
            await gemi_session.send_client_content(turns={"parts": [{"text": query}]})

            async for chunk in gemi_session.receive():
                if chunk.server_content:
                    if chunk.text is not None:
                        print(chunk.text)
                    # print(chunk.server_content)
                elif chunk.tool_call:
                    function_responses = []
                    for fc in chunk.tool_call.function_calls:
                        tool_id = fc.id
                        tool_name = fc.name
                        tool_args = fc.args
                        print(f"Using tool {tool_name} with args {tool_args}")
                        function_response = await self.session.call_tool(tool_name, tool_args)
                        formatted_response = types.FunctionResponse(
                                id=fc.id,
                                name=fc.name,
                                response={ "result": function_response.content[0].text} # simple, hard-coded function response
                            )
                        function_responses.append(formatted_response)
                        print(function_response.content[0].text)

                    await gemi_session.send_tool_response(function_responses=function_responses)




    async def chat_loop(self):
        """Run an interactive chat loop"""
        print("\nMCP Chatbot Started!")
        print("Type your queries or 'quit' to exit.")
        
        while True:
            try:
                query = input("\nQuery: ").strip()
        
                if query.lower() == 'quit':
                    break
                if query[0] == "@":
                    stripper = query[1:]
                    await self.get_resource(stripper)
                else:
                    await self.simple_chat(query)
                    print("\n")
                    
            except Exception as e:
                print(f"\nError: {str(e)}")
    
    async def cleanup(self): # new
        """Cleanly close all resources using AsyncExitStack."""
        await self.exit_stack.aclose()


async def main():
    chatbot = SimpleChatBot()
    try:
        await chatbot.connect_to_server() 
        await chatbot.chat_loop()
    finally:
        await chatbot.cleanup() #new! 


if __name__ == "__main__":
    asyncio.run(main())


        
            