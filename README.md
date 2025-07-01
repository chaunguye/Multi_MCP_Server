This is the demo that create an MCP Server Dynamically and Provide user a single endpoint for multiple MCP Server. 

There are 3 main components:
- MCP service (mcp_server_gen.py): this responsible for generate an MCP server script, add/remove tools in an exist server
- MCP Server: the generated mcp servers are stored in the folder user_mcp_server
- Mounting to FastAPI Server(main.py): mount the MCP Server to FastAPI Server at a specific endpoint.
- MCP Client(new_client.py): connect to the MCP Server through FastAPI Server.

Run flow:
- First generate the MCP Server by the command:

    python mcp_server_gen.py gen --tools <toolname> 

    (right now in toolsource we only have get_user_info and get_user_salary)
    This will create a server with the name user_retrieve_user<userid> (with user id is generated randomly)

  or you can add/remove tools on a exist server by:

    python mcp_server_gen.py mana --server <server_script> <add/remove> --tools <tool_name>

    EX: python mcp_server_gen.py mana --server user_retrieve_user891.py remove --tools get_user_info

- After that run the mounting service, this will mount the server under a specific path under FastAPI server. For example http://example.com/mcp-server/mcp:

    uvicorn main:app --reload

- Finally run the client, connect to the MCP Server through the FastAPI Server:

    uv run new_client.py