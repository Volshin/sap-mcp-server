"""Test script for MCP server"""
import asyncio
from anthropic import Anthropic
import os
from dotenv import load_dotenv

load_dotenv('.env')

client = Anthropic(api_key=os.getenv('CLAUDE_API_KEY'))


def test_mcp_tools():
    """Test MCP server tools"""
    
    print("🧪 Testing MCP Server\n")
    
    # Test 1: Get business partners
    print("Test 1: Get business partners")
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": "Use the get_business_partners tool to show me 5 business partners from SAP"
        }]
    )
    
    print(response.content[0].text)
    print("\n" + "="*50 + "\n")
    
    # Test 2: Search specific partner
    print("Test 2: Search for partner ID '11'")
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": "Use the search_partner tool to find details about partner with ID '11'"
        }]
    )
    
    print(response.content[0].text)


if __name__ == "__main__":
    test_mcp_tools()
