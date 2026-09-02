"""Tool registry for MCP and local tools."""

from app.tools.python_tool import PythonTool

TOOLS = {
    "python": PythonTool()
}

