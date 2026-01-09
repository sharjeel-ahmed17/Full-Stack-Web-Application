# OpenAI Agents SDK - MCP Integration

## Overview

The Model Context Protocol (MCP) provides a standardized way to connect AI models to different data sources and tools. The SDK supports four integration methods for MCP servers.

## Integration Methods

### 1. Hosted MCP Server Tools

Push tool execution into OpenAI's infrastructure using `HostedMCPTool`:

```python
from agents import Agent, HostedMCPTool

# Use hosted MCP server
agent = Agent(
    name="Assistant",
    instructions="Help users with various tasks",
    tools=[
        HostedMCPTool(
            server_url="https://mcp.example.com",
            tool_config={
                "api_key": "your_api_key",
                "timeout": 30
            }
        )
    ]
)
```

**Features:**
- Tools execute on OpenAI's servers
- No callbacks to your Python process
- Supports publicly reachable servers
- Streaming results with `Runner.run_streamed()`

### 2. Streamable HTTP MCP Servers

Manage network connections yourself with `MCPServerStreamableHttp`:

```python
from agents import MCPServerStreamableHttp

# HTTP MCP server with custom configuration
mcp_server = MCPServerStreamableHttp(
    url="https://mcp.example.com/api",
    headers={
        "Authorization": "Bearer token123",
        "X-Custom-Header": "value"
    },
    timeout=60,
    cache_tools_list=True,  # Cache tool list for performance
    max_retries=3
)

agent = Agent(
    name="Assistant",
    tools=[mcp_server]
)
```

**Features:**
- Custom headers and authentication
- Configurable timeouts
- Tool list caching
- Automatic retries
- Structured content support

### 3. HTTP with SSE MCP Servers

Server-Sent Events transport with `MCPServerSse`:

```python
from agents import MCPServerSse

# SSE-based MCP server
mcp_server = MCPServerSse(
    url="https://mcp.example.com/sse",
    headers={"Authorization": "Bearer token"},
    cache_tools_list=True
)

agent = Agent(
    name="Assistant",
    tools=[mcp_server]
)
```

**Features:**
- Real-time event streaming
- Same configuration as Streamable HTTP
- Ideal for long-running operations

### 4. Stdio MCP Servers

Launch local subprocess servers with `MCPServerStdio`:

```python
from agents import MCPServerStdio

# Local MCP server via subprocess
mcp_server = MCPServerStdio(
    command="python",
    args=["mcp_server.py"],
    env={
        "API_KEY": "key123",
        "CONFIG_PATH": "/path/to/config"
    }
)

agent = Agent(
    name="Assistant",
    tools=[mcp_server]
)
```

**Features:**
- Communicates via stdin/stdout
- Automatic process lifecycle management
- Useful for local development
- Command-line tools integration

## Tool Filtering

### Static Filtering

```python
from agents import create_static_tool_filter, MCPServerStreamableHttp

# Create tool filter
tool_filter = create_static_tool_filter(
    allowed_tool_names=["search", "analyze", "summarize"],
    blocked_tool_names=["delete", "admin"]
)

# Apply filter to MCP server
mcp_server = MCPServerStreamableHttp(
    url="https://mcp.example.com",
    tool_filter=tool_filter
)
```

### Dynamic Filtering

```python
from agents import ToolFilterContext

def dynamic_filter(context: ToolFilterContext) -> bool:
    """Filter tools based on context."""
    # Access agent information
    agent_name = context.agent.name

    # Access tool information
    tool_name = context.tool.name

    # Filter based on user permissions
    user_tier = context.user_data.get("tier", "free")
    if user_tier == "free" and tool_name.startswith("premium_"):
        return False

    return True

mcp_server = MCPServerStreamableHttp(
    url="https://mcp.example.com",
    tool_filter=dynamic_filter
)
```

## Connector-Based Servers

Use connector IDs with authorization:

```python
from agents import HostedMCPTool

mcp_tool = HostedMCPTool(
    connector_id="github_connector_v1",
    authorization_token="oauth_token_here"
)

agent = Agent(
    name="GitHub Assistant",
    instructions="Help with GitHub operations",
    tools=[mcp_tool]
)
```

## MCP Prompts

Servers can provide dynamic instructions:

```python
from agents import MCPServerStreamableHttp

mcp_server = MCPServerStreamableHttp(url="https://mcp.example.com")

# List available prompts
prompts = await mcp_server.list_prompts()
for prompt in prompts:
    print(f"Prompt: {prompt.name} - {prompt.description}")

# Get specific prompt
prompt = await mcp_server.get_prompt("research_workflow")
print(prompt.instructions)

# Use prompt in agent
agent = Agent(
    name="Researcher",
    instructions=prompt.instructions,
    tools=[mcp_server]
)
```

## Approval Workflows

Configure tool approval policies:

```python
from agents import HostedMCPTool, ApprovalPolicy

mcp_tool = HostedMCPTool(
    server_url="https://mcp.example.com",
    approval_policy=ApprovalPolicy.PER_TOOL  # Options: ALWAYS, NEVER, PER_TOOL
)

agent = Agent(
    name="Assistant",
    tools=[mcp_tool]
)
```

**Approval Policies:**
- **ALWAYS**: Require approval for all tool calls
- **NEVER**: Auto-approve all tool calls
- **PER_TOOL**: Configure approval per tool

## Performance Optimization

### Caching Tool Lists

```python
mcp_server = MCPServerStreamableHttp(
    url="https://mcp.example.com",
    cache_tools_list=True  # Cache tools to reduce latency
)
```

### Retry Configuration

```python
mcp_server = MCPServerStreamableHttp(
    url="https://mcp.example.com",
    max_retries=5,  # Retry failed requests
    timeout=120  # Longer timeout for slow operations
)
```

## Multiple MCP Servers

Use multiple MCP servers in a single agent:

```python
# Database MCP server
db_server = MCPServerStreamableHttp(
    url="https://db-mcp.example.com",
    cache_tools_list=True
)

# File system MCP server
fs_server = MCPServerStdio(
    command="python",
    args=["filesystem_mcp.py"]
)

# Web search MCP server
search_server = MCPServerStreamableHttp(
    url="https://search-mcp.example.com"
)

agent = Agent(
    name="Multi-Tool Assistant",
    instructions="Use database, filesystem, and web search tools",
    tools=[db_server, fs_server, search_server]
)
```

## Error Handling

```python
from agents.exceptions import MCPError

try:
    result = await Runner.run(agent, "Query MCP server")
except MCPError as e:
    print(f"MCP error: {e}")
    # Handle MCP-specific errors
```

## Tracing MCP Activity

The SDK automatically traces MCP operations:

```python
from agents import Runner, RunConfig

config = RunConfig(
    enable_tracing=True,
    trace_provider="openai"  # or custom provider
)

result = await Runner.run(
    agent,
    "Use MCP tools",
    config=config
)

# MCP activity will be captured in traces:
# - Tool listing
# - Tool invocations
# - Request/response details
```

## Complete Example

```python
from agents import Agent, Runner, MCPServerStreamableHttp, create_static_tool_filter

# Create MCP server with filtering
tool_filter = create_static_tool_filter(
    allowed_tool_names=["search", "fetch", "analyze"]
)

mcp_server = MCPServerStreamableHttp(
    url="https://mcp.example.com/api",
    headers={"Authorization": "Bearer secret_token"},
    timeout=60,
    cache_tools_list=True,
    max_retries=3,
    tool_filter=tool_filter
)

# Create agent with MCP server
agent = Agent(
    name="Research Assistant",
    instructions="Help users research topics using available tools",
    tools=[mcp_server]
)

# Use agent
result = await Runner.run(
    agent,
    "Research the history of AI agents"
)

print(result.final_output)
```

## Local Development Pattern

For development, use stdio MCP servers:

```python
# Development: Local stdio server
dev_server = MCPServerStdio(
    command="python",
    args=["dev_mcp_server.py", "--debug"],
    env={"ENV": "development"}
)

# Production: HTTP server
prod_server = MCPServerStreamableHttp(
    url="https://prod-mcp.example.com",
    cache_tools_list=True
)

# Use appropriate server based on environment
import os
mcp_server = dev_server if os.getenv("ENV") == "dev" else prod_server

agent = Agent(
    name="Assistant",
    tools=[mcp_server]
)
```

## Best Practices

1. **Cache Tool Lists**: Enable `cache_tools_list=True` for remote servers
2. **Filter Tools**: Use tool filters to limit exposed functionality
3. **Configure Timeouts**: Set appropriate timeouts for server latency
4. **Handle Errors**: Catch and handle `MCPError` exceptions
5. **Use Retries**: Configure `max_retries` for unreliable connections
6. **Secure Credentials**: Store API keys and tokens securely
7. **Enable Tracing**: Use tracing for debugging and monitoring
8. **Local Development**: Use stdio servers for local testing
9. **Production Readiness**: Use HTTP servers with caching for production
10. **Multiple Servers**: Combine MCP servers for comprehensive tooling

## MCP Server Creation

While this skill focuses on *using* MCP servers, you can create your own MCP servers:

```python
# Example MCP server structure (simplified)
class CustomMCPServer:
    def list_tools(self):
        """Return available tools."""
        return [
            {"name": "search", "description": "Search database"},
            {"name": "analyze", "description": "Analyze data"}
        ]

    async def invoke_tool(self, tool_name: str, params: dict):
        """Execute tool with parameters."""
        if tool_name == "search":
            return await self.search(params["query"])
        elif tool_name == "analyze":
            return await self.analyze(params["data"])
```

Refer to the MCP specification for complete server implementation details.
