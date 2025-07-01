
import json
import argparse
import os
import random

class ToolManager:

    def generate_tool_function(self,tool, serverName):
        tool_name = tool["name"]
        description = tool["description"]
        params = tool["inputSchema"]["properties"]
        param_list = ", ".join(params.keys())
        param_doc = "\n    ".join([
            f"{key}: {val.get('type', 'string')}"
            for key, val in params.items()
        ])
        
        # Function string with indentation
        func = f"""
@{serverName}.tool()
def {tool_name}({param_list}):
    \"\"\"
    {description}
    args:
        {param_doc}
    \"\"\"
    return f"{tool_name.replace('_', ' ').capitalize()} of {{{param_list}}} is example data"
"""
        return func

    def gen_mcp_server(self, tools):

        with open("tool-source.json", "r") as toolsource:
            json_source = json.load(toolsource)
            server_name = json_source.get("server_name")
            description = json_source.get("description", "")
            tool_required = tools if tools else None

            userId = random.randint(1,1000)
            server_inner = f"{server_name}_user{userId}"
            server_path = f"{server_inner}.py"

            mcp_server_directory = "./user_mcp_server"

            os.makedirs(mcp_server_directory, exist_ok=True)
            
            server_path = mcp_server_directory +"/"+ server_path

            with open(server_path, "x") as server_file:
                server_file.write("from fastmcp import FastMCP\n\n")
                server_file.write(f'{server_inner} = FastMCP("{server_inner}")\n')

                for tool in json_source.get("tools", []):
                    if tool_required is None or tool["name"] in tool_required:
                        tool_func = self.generate_tool_function(tool, server_inner)
                        server_file.write(tool_func)

                server_file.write(f"""
if __name__ == "__main__":
    {server_inner}.run(transport="http")
""")
    
    def manage_tools(self,serverPath, action, tools):
        lines = None
        tool_code= None
        userId = 123
        with open(f"./user_mcp_server/{serverPath}", "r") as server_file:
            lines = server_file.readlines()
        if lines is None:
            print("Server is not exist")
            return
        if action == "add":
            index = None
            for i, line in enumerate(lines):
                if line.strip().startswith("if __name__"):
                    index = i


            with open("tool-source.json", "r") as toolsource:
                json_source = json.load(toolsource)
                
                for tool in json_source.get("tools", []):
                    if tool["name"] in tools:
                        if tool_code is None:
                            tool_code = self.generate_tool_function(tool, serverPath[:-3])
                        else:
                            tool_code += self.generate_tool_function(tool, serverPath[:-3])
            
            final_lines = lines[:index] + [line for line in tool_code] + ["\n" ]+ lines[index:]
            with open(f"./user_mcp_server/{serverPath}", "w") as server_file:
                server_file.writelines(final_lines)
        elif action == "remove": 

            index = None
            list_to_delete = []
            found = False
            for i, line in enumerate(lines):    
                if any(line.strip().startswith(f"def {name}") for name in tools):
                    index = i
                    found = True
                if line.strip().startswith("return"):
                    if found:
                        list_to_delete += [(index, i)]
                        found = False

            final_lines = lines
            for delete_part in list_to_delete:
                final_lines = final_lines[0:delete_part[0]-1] + final_lines[delete_part[1]+1:]
            with open(f"./user_mcp_server/{serverPath}", "w") as server_file:
                server_file.writelines(final_lines)

        else:
            print("Action not supported")


def main():
    parser = argparse.ArgumentParser(description="Generate MCP server file with selected tools, or manage the tools in an exist MCP server")

    subparsers = parser.add_subparsers(dest="command", required=True)

    gen_parser = subparsers.add_parser("gen", help="Generate an MCP server")
    gen_parser.add_argument(
        "--tools", nargs="*", required=False,
        help="List of tool names to include in the server"
    )

    mana_parser = subparsers.add_parser("mana", help="Manage tools in existing server")
    mana_parser.add_argument(
        "--server", type=str, required=True,
        help="Specify whether to add or remove tools"
    )
    mana_parser.add_argument(
        "action", choices=["add", "remove"],
        help="Specify whether to add or remove tools"
    )
    mana_parser.add_argument(
        "--tools", nargs="+", required=True,
        help="List of tool names to add/remove"
    )
    args = parser.parse_args()

    tool_mana = ToolManager()
    if args.command == "gen":
        tool_mana.gen_mcp_server(args.tools)
        # print(args.tools)
    elif args.command == "mana":
        tool_mana.manage_tools(args.server, args.action, args.tools)
        # print(args.server, args.action, args.tools)
main()
