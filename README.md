# SAP MCP Server

Prototype MCP (Model Context Protocol) server that exposes SAP OData APIs as tools for LLM agents, allowing Claude to query and search SAP business partner data through natural language.

## What it does

- Connects to a SAP system via OData API (`A_BusinessPartner` entity set)
- Exposes two MCP tools: `get_business_partners` (list partners) and `search_partner` (lookup by ID)
- Runs as an MCP server over SSE (Server-Sent Events) transport
- Includes a test script demonstrating Claude calling the tools end-to-end

## Stack

Python, MCP SDK, Starlette, Uvicorn, Anthropic API, SAP OData

## Structure

- `sap_client.py` — SAP OData API client (business partner retrieval and search)
- `server.py` — MCP server exposing SAP client methods as tools, SSE transport
- `test_mcp.py` — test script calling the tools via Claude

## Setup

Requires a `.env` file with `SAP_API_KEY`, `SAP_BASE_URL`, and `CLAUDE_API_KEY` (not included).

## Status

Prototype / proof of concept, built while exploring SAP + AI agent integration patterns.
