"""Tool executor for running tools."""

from app.tools.registry import TOOLS


class ToolExecutor:
    """Executes registered tools."""

    def execute_tool(
        self,
        tool_name: str,
        tool_input: str
    ):
        """Execute a tool by name with given input."""

        tool = TOOLS.get(tool_name)

        if not tool:
            return {
                "success": False,
                "error": f"Unknown tool: {tool_name}"
            }

        return tool.execute(tool_input)

