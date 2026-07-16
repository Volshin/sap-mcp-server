"""MCP Server for SAP Integration using SSE transport"""
import os
import asyncio
from typing import Any
from mcp.server import Server
from mcp.server.sse import SseServerTransport
from mcp.types import Tool, TextContent
from dotenv import load_dotenv
import uvicorn
from starlette.applications import Starlette
from starlette.routing import Route

from sap_client import SAPClient

# Load environment variables
load_dotenv('.env')

# Configuration
SAP_API_KEY = os.getenv('SAP_API_KEY')
SAP_BASE_URL = os.getenv('SAP_BASE_URL')
MCP_HOST = os.getenv('MCP_HOST', 'localhost')
MCP_PORT = int(os.getenv('MCP_PORT', 8000))

# Initialize SAP client
sap_client = SAPClient(SAP_API_KEY, SAP_BASE_URL)

# Initialize MCP server
mcp_server = Server("sap-integration-server")


@mcp_server.list_tools()
async def list_tools() -> list[Tool]:
    """List available SAP tools"""
    return [
        Tool(
            name="get_business_partners",
            description="Get list of business partners from SAP system",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of partners to return (default: 10)",
                        "default": 10
                    }
                }
            }
        ),
        Tool(
            name="search_partner",
            description="Search for specific business partner by ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "partner_id": {
                        "type": "string",
                        "description": "Business Partner ID to search for"
                    }
                },
                "required": ["partner_id"]
            }
        )
    ]


@mcp_server.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Handle tool calls from Claude"""
    
    if name == "get_business_partners":
        limit = arguments.get("limit", 10)
        result = sap_client.get_business_partners(limit)
        
        return [TextContent(
            type="text",
            text=f"Business Partners from SAP:\n{result}"
        )]
    
    elif name == "search_partner":
        partner_id = arguments.get("partner_id")
        if not partner_id:
            return [TextContent(
                type="text",
                text="Error: partner_id is required"
            )]
        
        result = sap_client.search_partner(partner_id)
        return [TextContent(
            type="text",
            text=f"Business Partner Details:\n{result}"
        )]
    
    else:
        return [TextContent(
            type="text",
            text=f"Unknown tool: {name}"
        )]


async def handle_sse(request):
    """Handle SSE connections"""
    async with SseServerTransport("/messages") as transport:
        await mcp_server.run(
            transport.read_stream,
            transport.write_stream,
            mcp_server.create_initialization_options()
        )


# Create Starlette app
app = Starlette(
    routes=[
        Route("/sse", endpoint=handle_sse)
    ]
)


if __name__ == "__main__":
    print(f"🚀 Starting SAP MCP Server on {MCP_HOST}:{MCP_PORT}")
    print(f"📡 SSE endpoint: http://{MCP_HOST}:{MCP_PORT}/sse")
    print(f"🔗 SAP API: {SAP_BASE_URL}")
    print("\nPress Ctrl+C to stop")
    
    uvicorn.run(
        app,
        host=MCP_HOST,
        port=MCP_PORT,
        log_level="info"
    )
