# MCP Server - Configuration & Troubleshooting

## Claude Desktop Configuration

### Config File Location

**macOS:**
```
~/Library/Application Support/Claude/claude_desktop_config.json
```

**Windows:**
```
%APPDATA%\Claude\claude_desktop_config.json
```

**Linux:**
```
~/.config/Claude/claude_desktop_config.json
```

### Basic Configuration

```json
{
  "mcpServers": {
    "server-name": {
      "command": "command-to-run",
      "args": ["arg1", "arg2"],
      "env": {
        "ENV_VAR": "value"
      }
    }
  }
}
```

### Language-Specific Configurations

#### Python (uv)

```json
{
  "mcpServers": {
    "my-python-server": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/server",
        "run",
        "server.py"
      ],
      "env": {
        "PYTHONUNBUFFERED": "1"
      }
    }
  }
}
```

#### Python (system)

```json
{
  "mcpServers": {
    "my-python-server": {
      "command": "python3",
      "args": ["/absolute/path/to/server.py"],
      "env": {
        "API_KEY": "your-api-key",
        "ENVIRONMENT": "production"
      }
    }
  }
}
```

#### TypeScript/Node.js

```json
{
  "mcpServers": {
    "my-ts-server": {
      "command": "node",
      "args": ["/absolute/path/to/build/index.js"]
    }
  }
}
```

#### Java (Spring Boot)

```json
{
  "mcpServers": {
    "my-java-server": {
      "command": "java",
      "args": [
        "-Dspring.ai.mcp.server.stdio=true",
        "-jar",
        "/absolute/path/to/server.jar"
      ]
    }
  }
}
```

#### Kotlin

```json
{
  "mcpServers": {
    "my-kotlin-server": {
      "command": "java",
      "args": [
        "-jar",
        "/absolute/path/to/server-all.jar"
      ]
    }
  }
}
```

#### C# (.NET)

```json
{
  "mcpServers": {
    "my-dotnet-server": {
      "command": "dotnet",
      "args": [
        "run",
        "--project",
        "/absolute/path/to/project",
        "--no-build"
      ]
    }
  }
}
```

#### Rust

```json
{
  "mcpServers": {
    "my-rust-server": {
      "command": "/absolute/path/to/target/release/server"
    }
  }
}
```

### Multiple Servers

```json
{
  "mcpServers": {
    "file-server": {
      "command": "uv",
      "args": ["--directory", "/path/to/file-server", "run", "server.py"]
    },
    "database-server": {
      "command": "node",
      "args": ["/path/to/db-server/build/index.js"]
    },
    "api-server": {
      "command": "python3",
      "args": ["/path/to/api-server/server.py"],
      "env": {
        "API_KEY": "secret-key"
      }
    }
  }
}
```

## Environment Variables

### Common Variables

```json
{
  "mcpServers": {
    "my-server": {
      "command": "python3",
      "args": ["/path/to/server.py"],
      "env": {
        "API_KEY": "your-api-key",
        "DATABASE_URL": "postgresql://localhost/db",
        "LOG_LEVEL": "INFO",
        "ENVIRONMENT": "production",
        "TIMEOUT": "30"
      }
    }
  }
}
```

### Loading from .env Files

Server code can load environment variables:

```python
# Python
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("API_KEY")
```

```typescript
// TypeScript
import dotenv from "dotenv";
dotenv.config();

const API_KEY = process.env.API_KEY;
```

## Transport Configuration

### STDIO (Default)

Most common for local servers:

```python
# Python
def main():
    mcp.run(transport="stdio")
```

```typescript
// TypeScript
const transport = new StdioServerTransport();
await server.connect(transport);
```

### SSE (Server-Sent Events)

For web-based servers:

```python
# Python
from mcp.server.sse import SseServerTransport

def main():
    transport = SseServerTransport("/messages")
    mcp.run(transport=transport)
```

### HTTP

For REST-like APIs:

```python
# Python
from mcp.server.http import HttpServerTransport

def main():
    transport = HttpServerTransport(host="0.0.0.0", port=8000)
    mcp.run(transport=transport)
```

## Logging

### Python Logging

```python
import logging

# Configure logging to stderr (not stdout!)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()  # Defaults to stderr
    ]
)

logger = logging.getLogger(__name__)

@mcp.tool()
async def my_tool(param: str) -> str:
    logger.info(f"Tool called with param: {param}")
    try:
        result = await process(param)
        logger.info("Tool completed successfully")
        return result
    except Exception as e:
        logger.error(f"Tool failed: {e}", exc_info=True)
        raise
```

### TypeScript Logging

```typescript
// Write to stderr, not stdout
console.error("Server starting...");
console.error(`Processing request: ${requestId}`);

// Or use a logging library
import winston from "winston";

const logger = winston.createLogger({
  transports: [
    new winston.transports.Console({
      stderrLevels: ["error", "warn", "info", "debug"]
    })
  ]
});

logger.info("Server started");
```

## Troubleshooting

### Check Logs

**macOS/Linux:**
```bash
tail -f ~/Library/Logs/Claude/mcp*.log
```

**Windows:**
```powershell
Get-Content "$env:APPDATA\Claude\Logs\mcp*.log" -Wait
```

### Common Issues

#### 1. Server Not Appearing

**Symptoms:** Server doesn't show up in Claude

**Solutions:**
- Verify JSON syntax in config file
- Use absolute paths (no `~` or relative paths)
- Restart Claude properly (Cmd+Q on macOS, not just close window)
- Check server builds without errors
- Verify command is in PATH

**Test:**
```bash
# Manually run the command from config
/absolute/path/to/command arg1 arg2
```

#### 2. Tools/Resources Not Working

**Symptoms:** Server appears but tools don't execute

**Solutions:**
- Check tool registration code
- Verify JSON schemas are valid
- Review server logs for errors
- Test tool functions independently

**Debug:**
```python
# Add logging to tool
@mcp.tool()
async def my_tool(param: str) -> str:
    logger.info(f"Tool called: my_tool({param})")
    try:
        result = await implementation(param)
        logger.info(f"Tool result: {result}")
        return result
    except Exception as e:
        logger.error(f"Tool error: {e}", exc_info=True)
        raise
```

#### 3. Invalid JSON Error

**Symptoms:** "Invalid JSON" errors in logs

**Causes:**
- Writing to stdout in stdio transport
- Malformed JSON-RPC messages

**Solutions:**
```python
# Wrong - writes to stdout
print("Debug message")

# Correct - writes to stderr
import logging
logging.info("Debug message")

# Also correct
import sys
print("Debug message", file=sys.stderr)
```

#### 4. Permission Denied

**Symptoms:** "Permission denied" or "Command not found"

**Solutions:**
- Check file permissions: `chmod +x /path/to/server`
- Verify command exists: `which python3`
- Use absolute paths in config
- Check directory permissions

#### 5. Module Not Found

**Symptoms:** Import errors or missing dependencies

**Solutions:**
- Install dependencies: `pip install -r requirements.txt`
- Use virtual environment
- Verify package installation: `pip list`
- Check PYTHONPATH/NODE_PATH

#### 6. Server Timeout

**Symptoms:** Server takes too long to start

**Solutions:**
- Reduce startup time (defer heavy initialization)
- Check network connectivity
- Review database connection timeouts
- Optimize imports

#### 7. Environment Variables Not Set

**Symptoms:** Server can't access API keys or configs

**Solutions:**
- Add env vars to claude_desktop_config.json
- Use .env files in server code
- Check variable names (case-sensitive)
- Verify values are strings

### Testing Servers Independently

Test server before Claude integration:

```bash
# Run server and send test message
echo '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}' | python server.py

# Expected output (JSON-RPC response):
# {"jsonrpc":"2.0","id":1,"result":{"tools":[...]}}
```

### Debugging Checklist

- [ ] Config file syntax is valid JSON
- [ ] All paths are absolute
- [ ] Server builds/runs independently
- [ ] No stdout writes in stdio transport
- [ ] Dependencies are installed
- [ ] Environment variables are set
- [ ] Permissions are correct
- [ ] Claude restarted properly

### Getting Help

1. **Check logs first**: Most issues show up in logs
2. **Test independently**: Run server outside Claude
3. **Simplify**: Start with minimal server, add features incrementally
4. **Community**: https://modelcontextprotocol.io/community
5. **GitHub Issues**: https://github.com/modelcontextprotocol

## Production Deployment

### Security

```python
# Validate inputs
@mcp.tool()
async def execute_query(query: str) -> str:
    # Prevent SQL injection
    if "DROP" in query.upper() or "DELETE" in query.upper():
        return "Dangerous operations not allowed"

    # Use parameterized queries
    result = await db.execute_safe(query)
    return result
```

### Rate Limiting

```python
from collections import defaultdict
from time import time

request_counts = defaultdict(list)

async def rate_limit(client_id: str, max_requests: int = 10, window: int = 60):
    """Rate limit by client ID."""
    now = time()
    # Remove old requests
    request_counts[client_id] = [
        req_time for req_time in request_counts[client_id]
        if now - req_time < window
    ]

    if len(request_counts[client_id]) >= max_requests:
        raise Exception("Rate limit exceeded")

    request_counts[client_id].append(now)
```

### Error Handling

```python
@mcp.tool()
async def robust_tool(param: str) -> str:
    """Tool with comprehensive error handling."""
    try:
        # Validate input
        if not param:
            return "Error: Parameter is required"

        # Process with timeout
        result = await asyncio.wait_for(
            process(param),
            timeout=30.0
        )

        return result

    except asyncio.TimeoutError:
        logger.error("Operation timed out")
        return "Error: Operation timed out. Please try again."

    except ValidationError as e:
        logger.warning(f"Validation failed: {e}")
        return f"Error: Invalid input - {str(e)}"

    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        return "Error: An unexpected error occurred. Please contact support."
```

### Monitoring

```python
from prometheus_client import Counter, Histogram
import time

tool_calls = Counter('mcp_tool_calls_total', 'Total tool calls', ['tool_name'])
tool_duration = Histogram('mcp_tool_duration_seconds', 'Tool execution time', ['tool_name'])

@mcp.tool()
async def monitored_tool(param: str) -> str:
    """Tool with monitoring."""
    tool_calls.labels(tool_name='monitored_tool').inc()

    start_time = time.time()
    try:
        result = await process(param)
        return result
    finally:
        duration = time.time() - start_time
        tool_duration.labels(tool_name='monitored_tool').observe(duration)
```

## Advanced Configuration

### Custom Server Capabilities

```python
from mcp.server import Server
from mcp.types import ServerCapabilities

server = Server(
    name="advanced-server",
    version="1.0.0",
    capabilities=ServerCapabilities(
        tools=True,
        resources=True,
        prompts=True,
        logging=True
    )
)
```

### Dynamic Server Registration

Servers can register capabilities at runtime:

```python
# Start with basic capabilities
mcp = FastMCP("dynamic-server")

# Register tools dynamically
async def load_plugins():
    plugins = discover_plugins()
    for plugin in plugins:
        mcp.register_tool(plugin.tool_function)
```

### Multi-Transport Servers

Run same server on multiple transports:

```python
import asyncio

async def run_stdio():
    mcp_stdio = FastMCP("server")
    mcp_stdio.run(transport="stdio")

async def run_http():
    mcp_http = FastMCP("server")
    mcp_http.run(transport=HttpServerTransport(port=8000))

# Run both
asyncio.gather(run_stdio(), run_http())
```

## Best Practices

1. **Use absolute paths** in configuration
2. **Never write to stdout** for stdio servers
3. **Log to stderr** for debugging
4. **Handle errors gracefully** with user-friendly messages
5. **Validate all inputs** before processing
6. **Test independently** before Claude integration
7. **Monitor production servers** with logging and metrics
8. **Rate limit** to prevent abuse
9. **Use environment variables** for secrets
10. **Document your server** with clear tool/resource descriptions

## Next Steps

- Review **server-implementation.md** for language-specific patterns
- See **tools.md** for implementing tools
- See **resources.md** for exposing data
- See **prompts.md** for creating templates
