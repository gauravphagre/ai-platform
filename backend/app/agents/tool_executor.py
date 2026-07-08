from app.agents.tool_registry import TOOLS


class ToolExecutor:

    def execute_tool(
        self,
        tool_name: str,
        tool_input: str
    ):

        tool = TOOLS.get(tool_name)

        if not tool:

            return {
                "success": False,
                "error": f"Unknown tool: {tool_name}"
            }

        return tool.execute(tool_input)