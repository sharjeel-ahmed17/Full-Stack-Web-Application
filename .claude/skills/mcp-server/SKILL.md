---
name: mcp-server
description: Comprehensive guide for building Model Context Protocol (MCP) servers. Use when Claude needs to work with MCP servers for (1) creating MCP servers in any language (Python, TypeScript, Java, Kotlin, C#, Rust), (2) implementing tools (callable functions), (3) exposing resources (data sources), (4) creating prompts (reusable templates), (5) configuring Claude Desktop integration, (6) choosing transport mechanisms (stdio, SSE, HTTP), (7) troubleshooting MCP server issues, or any other MCP server development tasks.
license: Complete terms in LICENSE.txt
---

# MCP Server Development

## Overview

The Model Context Protocol (MCP) is an open-source standard for connecting AI applications to external systems. Think of it as **USB-C for AI** — providing a standardized way to connect Claude and other AI models to data sources, tools, and workflows.

### Key Capabilities

MCP servers can expose three types of capabilities:

| Capability | Control | Purpose | Examples |
|------------|---------|---------|----------|
| **Tools** | Model | Functions the LLM can actively call | search, calculate, send_email |
| **Resources** | Application | Read-only data sources for context | files, database records, API responses |
| **Prompts** | User | Pre-built templates for specific workflows | code-review, plan-vacation |

## Quick Navigation

Use the following reference files based on your needs:

- **Getting started**: See [quickstart.md](references/quickstart.md) for installation, basic setup, and first server
- **Language-specific implementation**: See [server-implementation.md](references/server-implementation.md) for detailed patterns in Python, TypeScript, Java, Kotlin, C#, Rust
- **Implementing tools**: See [tools.md](references/tools.md) for creating callable functions with schemas
- **Exposing resources**: See [resources.md](references/resources.md) for providing data sources
- **Creating prompts**: See [prompts.md](references/prompts.md) for reusable templates
- **Configuration & troubleshooting**: See [configuration.md](references/configuration.md) for Claude Desktop setup and debugging

## Architecture

```
┌─────────────┐          MCP Protocol          ┌──────────────┐
│ AI Client   │◄─────────────────────────────►│ MCP Server   │
│ (Claude)    │     (JSON-RPC over           │ (Your code)  │
│             │      stdio/SSE/HTTP)         │              │
└─────────────┘                               └──────────────┘
```

- **Client**: AI application (Claude Desktop, custom apps)
- **Server**: Your code exposing capabilities via MCP
- **Protocol**: JSON-RPC messages over stdio, SSE, or HTTP

## Decision Tree

Follow this tree to find the right approach:

```
What do you need to build?

├─ New MCP server from scratch
│  ├─ Quick prototype → Python (FastMCP)
│  ├─ Web application → TypeScript
│  ├─ Enterprise/Spring → Java
│  ├─ Modern JVM → Kotlin
│  ├─ .NET ecosystem → C#
│  └─ High performance → Rust
│
│  Reference: quickstart.md, server-implementation.md
│
├─ Add capabilities to existing server
│  ├─ Callable functions → Implement tools
│  │  Reference: tools.md
│  │
│  ├─ Data access → Implement resources
│  │  Reference: resources.md
│  │
│  └─ Workflow templates → Implement prompts
│     Reference: prompts.md
│
├─ Claude Desktop integration
│  └─ Configuration, troubleshooting
│     Reference: configuration.md
│
└─ Debugging server issues
   └─ Logs, common errors, solutions
      Reference: configuration.md
```

## Language Selection Guide

### Python (FastMCP) - Recommended for Most Cases

**Best for:** Quick prototypes, data science, API integrations

**Pros:**
- Fastest to get started
- Simple, intuitive API
- Great for data processing
- Excellent async support

**Example:**
```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("my-server")

@mcp.tool()
async def search(query: str) -> str:
    """Search for information."""
    return f"Results for: {query}"

mcp.run(transport="stdio")
```

**Reference:** server-implementation.md (Python section)

### TypeScript

**Best for:** Web applications, Node.js services, existing TS projects

**Pros:**
- Type safety
- Great ecosystem
- Web integration
- Native async/await

**Reference:** server-implementation.md (TypeScript section)

### Java (Spring AI)

**Best for:** Enterprise applications, existing Spring projects

**Pros:**
- Enterprise-ready
- Spring ecosystem
- Strong typing
- Mature tooling

**Reference:** server-implementation.md (Java section)

### Kotlin

**Best for:** Modern JVM applications, Android

**Pros:**
- Modern language features
- Coroutines
- Null safety
- Java interop

**Reference:** server-implementation.md (Kotlin section)

### C# (.NET)

**Best for:** .NET applications, Windows services

**Pros:**
- .NET ecosystem
- Strong typing
- Great tooling
- Cross-platform

**Reference:** server-implementation.md (C# section)

### Rust

**Best for:** High-performance servers, systems programming

**Pros:**
- Maximum performance
- Memory safety
- No runtime overhead
- Excellent concurrency

**Reference:** server-implementation.md (Rust section)

## Common Workflows

### 1. Simple Tool Server

**When to use**: Expose callable functions to Claude

**Pattern**:
```python
@mcp.tool()
async def calculate(expression: str) -> float:
    """Evaluate mathematical expression."""
    return eval(expression)  # Use safe eval in production
```

**Reference**: tools.md

### 2. Data Access Server

**When to use**: Provide read access to files, databases, APIs

**Pattern**:
```python
@mcp.resource("file:///{path}")
async def read_file(path: str) -> str:
    """Read file contents."""
    with open(path, "r") as f:
        return f.read()
```

**Reference**: resources.md

### 3. Workflow Template Server

**When to use**: Provide reusable prompt templates

**Pattern**:
```python
@mcp.prompt()
def code_review() -> str:
    """Perform thorough code review."""
    return "Review this code for quality, bugs, and improvements."
```

**Reference**: prompts.md

### 4. Full-Featured Server

**When to use**: Combine tools, resources, and prompts

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("full-server")

# Tools
@mcp.tool()
async def search(query: str) -> str:
    return await perform_search(query)

# Resources
@mcp.resource("data://records/{id}")
async def get_record(id: str) -> str:
    return await fetch_record(id)

# Prompts
@mcp.prompt()
def analyze() -> str:
    return "Analyze the data using available resources and tools."

mcp.run(transport="stdio")
```

**Reference**: All reference files

## Transport Selection

### STDIO (Recommended for Local Servers)

**Use case**: Claude Desktop integration

**Setup**:
```python
mcp.run(transport="stdio")
```

**Claude config**:
```json
{
  "mcpServers": {
    "my-server": {
      "command": "python",
      "args": ["/path/to/server.py"]
    }
  }
}
```

**Critical Rule**: Never write to stdout - it corrupts the protocol. Use stderr for logging.

### SSE (Server-Sent Events)

**Use case**: Web applications, real-time updates

**Setup**:
```python
from mcp.server.sse import SseServerTransport
mcp.run(transport=SseServerTransport("/messages"))
```

### HTTP

**Use case**: RESTful APIs, cloud deployments

**Setup**:
```python
from mcp.server.http import HttpServerTransport
mcp.run(transport=HttpServerTransport(host="0.0.0.0", port=8000))
```

## Quick Start Example

### 1. Create Server (server.py)

```python
from mcp.server.fastmcp import FastMCP
import logging

logging.basicConfig(level=logging.INFO)
mcp = FastMCP("hello-server")

@mcp.tool()
async def greet(name: str) -> str:
    """Greet someone by name."""
    logging.info(f"Greeting {name}")
    return f"Hello, {name}!"

@mcp.resource("info://version")
async def get_version() -> str:
    """Get server version."""
    return "1.0.0"

@mcp.prompt()
def friendly_chat() -> str:
    """Start a friendly conversation."""
    return "Let's have a friendly chat. How are you today?"

def main():
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()
```

### 2. Configure Claude Desktop

Edit `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "hello-server": {
      "command": "python3",
      "args": ["/absolute/path/to/server.py"]
    }
  }
}
```

### 3. Restart Claude

Quit Claude completely (Cmd+Q on macOS) and reopen.

### 4. Test

Ask Claude:
- "Can you greet Alice?"
- "What's the server version?"
- "Let's use the friendly chat prompt"

## Critical Rules

### 1. NEVER Write to stdout (stdio Transport)

❌ **Wrong:**
```python
print("Debug message")  # Breaks the protocol!
```

✅ **Correct:**
```python
import logging
logging.info("Debug message")  # Writes to stderr
```

### 2. Always Use Absolute Paths

❌ **Wrong:**
```json
{
  "command": "~/server/run.sh"
}
```

✅ **Correct:**
```json
{
  "command": "/Users/username/server/run.sh"
}
```

### 3. Validate All Inputs

```python
@mcp.tool()
async def divide(a: float, b: float) -> float:
    """Divide two numbers."""
    if b == 0:
        return "Error: Division by zero"
    return a / b
```

### 4. Handle Errors Gracefully

```python
@mcp.tool()
async def api_call(endpoint: str) -> str:
    """Call external API."""
    try:
        result = await call_api(endpoint)
        return result
    except TimeoutError:
        return "Error: Request timed out"
    except Exception as e:
        return f"Error: {str(e)}"
```

## Troubleshooting

### Server Not Appearing

1. Check config JSON syntax
2. Use absolute paths
3. Restart Claude properly (Cmd+Q)
4. Check logs: `tail -f ~/Library/Logs/Claude/mcp*.log`

### Tools Not Working

1. Verify tool registration
2. Check JSON schema is valid
3. Review server logs
4. Test tool function independently

### "Invalid JSON" Error

- Likely writing to stdout in stdio transport
- Use logging to stderr instead

**Reference**: configuration.md for complete troubleshooting guide

## Best Practices

### Server Design

1. **Clear Naming**: Use descriptive names for tools/resources/prompts
2. **Good Descriptions**: Explain what each capability does and when to use it
3. **Input Validation**: Always validate parameters before processing
4. **Error Messages**: Return helpful, user-friendly error messages
5. **Logging**: Log to stderr for debugging (never stdout in stdio)

### Security

1. **Validate Inputs**: Prevent injection attacks
2. **Sanitize Paths**: Prevent directory traversal
3. **Rate Limiting**: Prevent abuse
4. **Environment Variables**: Never hardcode secrets

### Performance

1. **Async Operations**: Use async for I/O operations
2. **Caching**: Cache expensive operations
3. **Timeouts**: Set reasonable timeouts
4. **Resource Limits**: Limit response sizes

### Testing

1. **Unit Tests**: Test tools/resources independently
2. **Integration Tests**: Test full server functionality
3. **Manual Testing**: Run server directly before Claude integration
4. **Log Review**: Check logs for errors and warnings

## Multi-Server Architecture

Claude can connect to multiple MCP servers simultaneously:

```json
{
  "mcpServers": {
    "file-server": {
      "command": "python",
      "args": ["/path/to/file-server.py"]
    },
    "database-server": {
      "command": "node",
      "args": ["/path/to/db-server/index.js"]
    },
    "api-server": {
      "command": "java",
      "args": ["-jar", "/path/to/api-server.jar"]
    }
  }
}
```

Claude can use tools and resources from all servers in a single conversation.

## Development Workflow

1. **Design**: Identify what capabilities to expose
2. **Implement**: Write server code with tools/resources/prompts
3. **Test Independently**: Run and test server outside Claude
4. **Configure**: Add to Claude Desktop config
5. **Test in Claude**: Verify integration works
6. **Iterate**: Refine based on usage
7. **Deploy**: Deploy to production with monitoring

## Additional Resources

- **Official Documentation**: https://modelcontextprotocol.io/docs
- **GitHub**: https://github.com/modelcontextprotocol
- **Community**: https://modelcontextprotocol.io/community
- **Specification**: https://modelcontextprotocol.io/specification

## Reference Files Summary

All reference files are in the `references/` directory:

1. **quickstart.md** - Installation and basic setup (~300 lines)
2. **server-implementation.md** - Language-specific patterns for all 6 languages (~600 lines)
3. **tools.md** - Implementing callable functions (~400 lines)
4. **resources.md** - Exposing data sources (~350 lines)
5. **prompts.md** - Creating reusable templates (~300 lines)
6. **configuration.md** - Claude Desktop config and troubleshooting (~400 lines)

Load reference files as needed based on the specific task requirements.
