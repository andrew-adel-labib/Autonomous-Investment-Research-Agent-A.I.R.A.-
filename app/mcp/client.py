from app.mcp.tool_router import call_tool


class MCPClient:

    def call(self, tool_name: str, params: dict):
        return call_tool(tool_name, params)