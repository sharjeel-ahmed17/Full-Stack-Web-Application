# MCP Server - Quick Start

## What is MCP?

The Model Context Protocol (MCP) is an open-source standard for connecting AI applications to external systems. Think of it as **USB-C for AI applications** — providing a standardized way to connect Claude and other AI models to:

- **Data sources**: Files, databases, APIs
- **Tools**: Search engines, calculators, custom functions
- **Workflows**: Specialized prompts and operations

## Architecture

MCP uses a client-server architecture:

```
┌─────────────┐          MCP Protocol          ┌──────────────┐
│ AI Client   │◄─────────────────────────────►│ MCP Server   │
│ (Claude)    │     (JSON-RPC over           │ (Your tools) │
│             │      stdio/SSE/HTTP)         │              │
└─────────────┘                               └──────────────┘
```

- **Client**: AI application (Claude Desktop, custom apps)
- **Server**: Your code exposing capabilities via MCP protocol
- **Protocol**: JSON-RPC messages over stdio, SSE, or HTTP

## Server Capabilities

MCP servers can provide:

1. **Tools**: Functions the AI can call (search, calculate, send email)
2. **Resources**: Data the AI can read (files, database records)
3. **Prompts**: Pre-configured templates (specialized workflows)

## Choosing a Language

Select based on your project needs:

| Language | Best For | SDK |
|----------|----------|-----|
| **Python** | Quick prototypes, data science | FastMCP (recommended) |
| **TypeScript** | Web apps, Node.js services | Official SDK |
| **Java** | Enterprise, Spring apps | Spring AI |
| **Kotlin** | Modern JVM apps | Official Kotlin SDK |
| **C#** | .NET applications | Official .NET SDK |
| **Rust** | High performance, systems | rmcp crate |

## Quick Example (Python)

### 1. Installation

```bash
# Install uv (package manager)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create project
uv init my-server
cd my-server

# Install dependencies
uv add "mcp[cli]"
```

### 2. Create Server (server.py)

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("my-server")

@mcp.tool()
async def greet(name: str) -> str:
    """Greet someone by name.

    Args:
        name: The person's name
    """
    return f"Hello, {name}!"

@mcp.tool()
async def add(a: int, b: int) -> int:
    """Add two numbers.

    Args:
        a: First number
        b: Second number
    """
    return a + b

def main():
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()
```

### 3. Configure Claude Desktop

Edit `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "my-server": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/my-server",
        "run",
        "server.py"
      ]
    }
  }
}
```

### 4. Restart Claude

1. Quit Claude completely (Cmd+Q on macOS)
2. Reopen Claude Desktop
3. Test: "Can you greet John?" or "What's 5 + 3?"

## Quick Example (TypeScript)

### 1. Setup

```bash
mkdir my-server
cd my-server
npm init -y
npm install @modelcontextprotocol/sdk zod
npm install -D @types/node typescript
```

### 2. Create Server (src/index.ts)

```typescript
#!/usr/bin/env node
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const server = new Server({
  name: "my-server",
  version: "1.0.0",
});

server.setRequestHandler("tools/list", async () => ({
  tools: [
    {
      name: "greet",
      description: "Greet someone by name",
      inputSchema: {
        type: "object",
        properties: {
          name: { type: "string", description: "Person's name" },
        },
        required: ["name"],
      },
    },
  ],
}));

server.setRequestHandler("tools/call", async (request) => {
  if (request.params.name === "greet") {
    const { name } = request.params.arguments as { name: string };
    return {
      content: [
        {
          type: "text",
          text: `Hello, ${name}!`,
        },
      ],
    };
  }
  throw new Error(`Unknown tool: ${request.params.name}`);
});

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("My Server running on stdio");
}

main().catch(console.error);
```

### 3. Configure package.json

```json
{
  "type": "module",
  "bin": {
    "my-server": "./build/index.js"
  },
  "scripts": {
    "build": "tsc && chmod +x build/index.js"
  }
}
```

### 4. Build and Configure

```bash
npm run build
```

Add to Claude config:
```json
{
  "mcpServers": {
    "my-server": {
      "command": "node",
      "args": ["/absolute/path/to/my-server/build/index.js"]
    }
  }
}
```

## Transport Types

MCP supports three transport mechanisms:

### 1. STDIO (Standard Input/Output)
- **Use case**: Local servers, command-line tools
- **How it works**: Server runs as subprocess, JSON-RPC via stdin/stdout
- **Best for**: Claude Desktop integration

### 2. SSE (Server-Sent Events)
- **Use case**: Web applications, streaming updates
- **How it works**: HTTP-based event streaming
- **Best for**: Real-time data, web integrations

### 3. HTTP
- **Use case**: RESTful APIs, cloud deployments
- **How it works**: Traditional request-response
- **Best for**: Distributed systems, microservices

## Critical: STDIO Logging Rules

**NEVER write to stdout** in stdio servers - it corrupts the JSON-RPC protocol.

❌ **Wrong:**
```python
print("Processing...")  # Breaks the protocol!
```

✅ **Correct:**
```python
import logging
logging.info("Processing...")  # Writes to stderr
```

For other languages:
```typescript
console.error("Message");  // TypeScript - use stderr
```

```java
System.err.println("Message");  // Java
```

```rust
eprintln!("Message");  // Rust
```

## Troubleshooting

### Server Not Appearing in Claude

1. **Check config syntax**: Validate JSON
2. **Use absolute paths**: No relative paths or ~
3. **Restart properly**: Cmd+Q (not just close window)
4. **Check logs**:
   ```bash
   tail -f ~/Library/Logs/Claude/mcp*.log
   ```

### Tools Not Working

1. **Verify server builds**: Run build commands without errors
2. **Check tool schemas**: Ensure JSON Schema is valid
3. **Review logs**: Look for error messages
4. **Test independently**: Run server directly to test

### Common Errors

- **"Command not found"**: Check absolute path in config
- **"Invalid JSON"**: Likely stdout corruption (see logging rules)
- **"Server timeout"**: Server taking too long to start

## Next Steps

See detailed reference files for:

- **server-implementation.md**: Language-specific server patterns
- **tools.md**: Implementing tools with validation
- **resources.md**: Exposing data sources
- **prompts.md**: Creating prompt templates
- **configuration.md**: Advanced config and deployment

## Additional Resources

- **Documentation**: https://modelcontextprotocol.io/docs
- **GitHub**: https://github.com/modelcontextprotocol
- **Community**: https://modelcontextprotocol.io/community
