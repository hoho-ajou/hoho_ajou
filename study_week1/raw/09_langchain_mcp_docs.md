# Model Context Protocol (MCP) in LangChain

원문: https://docs.langchain.com/oss/python/langchain/mcp

## Overview
The documentation describes how to connect LangChain agents to MCP servers using `MCPAdapter`, built on FastMCP. "Model Context Protocol (MCP) is an open protocol that standardizes how applications provide tools and context to language models."

## Installation
```bash
pip install "langchain[mcp]"
```

## Basic Usage
1. Opening an `MCPAdapter` with a target
2. Calling `list_tools()` to discover available tools
3. Building an agent with `create_agent()` and the discovered tools

## Supported Transport Types
`MCPAdapter` automatically infers transport from the target provided:
- HTTP/HTTPS URLs (str): Remote connections over streamable HTTP
- Script paths (Path): Local scripts launched as subprocesses over stdio
- Transport objects: Pre-configured StreamableTransport instances
- In-process FastMCP servers: Direct in-memory connection
- MCPConfig dictionaries: Multiple servers via one adapter
- Prebuilt FastMCP clients: For advanced control over configuration

## Important Notes
Requires "langchain[mcp]>=1.4.0 and is in beta." String targets must be valid URLs to prevent accidental subprocess launches of local files.
