# Model Context Protocol (MCP): A Comprehensive Introduction (Stytch)

원문: https://stytch.com/blog/model-context-protocol-introduction/

## What is MCP?
MCP is fundamentally "a common protocol" built on JSON-RPC 2.0 that allows AI assistants to invoke functions, fetch data, or use predefined prompts from external services, providing "one standardized 'language' for all interactions."

The protocol operates through a client-server architecture where AI-powered applications run an MCP client component while external integrations function as MCP servers.

## Key Value Propositions
- Rapid Tool Integration: plug-and-play capability additions without custom-coding each integration
- Autonomous Agents: agents retrieve info and perform multi-step actions (e.g. CRM → email → database log)
- Reduced Friction: single mechanism instead of separate integrations per service
- Consistency: uniform JSON structure across tools
- Two-Way Context: Prompts (templates) + Resources (data context), not just one-shot API calls

## Architecture
- MCP Client: embedded in AI applications
- MCP Server: exposes functions, resources, prompts via JSON-RPC

Example tools/list request:
```json
{"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {}}
```

## Comparison to Other Approaches
- Custom integrations: labor-intensive, non-scalable, per-service code
- ChatGPT Plugins (2023): proprietary, platform-specific, mostly one-shot calls
- LangChain-style frameworks: developer-facing standard via Python classes, still custom per tool. MCP shifts standardization to be model-facing, enabling dynamic runtime discovery.

## Technical Flow
1. Connect to MCP Server (stdio locally or HTTP stream remotely)
2. Discover Tools/Resources (tools/list)
3. LLM chooses tool via function calling
4. Invoke Tool via MCP (tools/call with name + arguments)
5. Return Result to LLM, integrated into response

## Authentication Evolution
Early MCP (late 2024) lacked standardized auth for remote servers — required local/trusted execution or manually supplied credentials. OAuth 2.0 adoption added: Dynamic Client Registration, Automatic Endpoint Discovery, secure token management scoped to permissions, multi-user support.

## Debugging
MCP Inspector: interactive tool for testing/inspecting servers, viewing client-server interactions.

## Real-World Applications
AI chatbots accessing external data, AI-driven workflow automation, cross-industry automation (finance, healthcare, manufacturing).
