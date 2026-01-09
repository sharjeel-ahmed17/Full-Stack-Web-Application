# MCP Server - Resources Reference

## What Are Resources?

**Resources** provide structured access to data. Unlike tools (which the AI calls), resources are application-controlled data sources that provide read-only context.

### Protocol Operations

```
resources/list           → List available direct resources
resources/templates/list → List resource templates
resources/read           → Retrieve resource contents
resources/subscribe      → Monitor resource changes
```

## Resource Types

### 1. Direct Resources
Fixed URIs pointing to specific data:
```
file:///project/README.md
calendar://events/2024
database://users/table
```

### 2. Resource Templates
Dynamic URIs with parameters for flexible queries:
```
travel://activities/{city}/{category}
weather://forecast/{city}/{date}
github://repos/{owner}/{repo}/issues
```

## Python Implementation

### Direct Resource

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("docs-server")

@mcp.resource("file:///docs/readme")
async def get_readme() -> str:
    """Get the project README file."""
    with open("README.md", "r") as f:
        return f.read()

@mcp.resource("database://users/count")
async def get_user_count() -> str:
    """Get total number of users."""
    count = await db.count_users()
    return f"Total users: {count}"
```

### Resource Template

```python
@mcp.resource("file:///{path}")
async def get_file(path: str) -> str:
    """Read any file from the project.

    Args:
        path: Relative path to file
    """
    file_path = BASE_DIR / path
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    with open(file_path, "r") as f:
        return f.read()

@mcp.resource("github://repos/{owner}/{repo}/readme")
async def get_github_readme(owner: str, repo: str) -> str:
    """Fetch README from GitHub repository."""
    url = f"https://api.github.com/repos/{owner}/{repo}/readme"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        data = response.json()
        # Decode base64 content
        import base64
        content = base64.b64decode(data["content"]).decode()
        return content
```

### Resource with Metadata

```python
from mcp.types import ResourceContents, TextResourceContents

@mcp.resource("api://data/{dataset}")
async def get_dataset(dataset: str) -> ResourceContents:
    """Get dataset with metadata."""
    data = await fetch_dataset(dataset)

    return TextResourceContents(
        uri=f"api://data/{dataset}",
        mimeType="application/json",
        text=json.dumps(data, indent=2)
    )
```

## TypeScript Implementation

### Direct Resource

```typescript
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { ListResourcesRequestSchema, ReadResourceRequestSchema } from "@modelcontextprotocol/sdk/types.js";

const server = new Server({ name: "docs-server", version: "1.0.0" });

// List resources
server.setRequestHandler(ListResourcesRequestSchema, async () => ({
  resources: [
    {
      uri: "file:///docs/readme",
      name: "Project README",
      description: "Main project documentation",
      mimeType: "text/markdown"
    },
    {
      uri: "file:///docs/api",
      name: "API Documentation",
      description: "API reference documentation",
      mimeType: "text/markdown"
    }
  ]
}));

// Read resource
server.setRequestHandler(ReadResourceRequestSchema, async (request) => {
  const uri = request.params.uri;

  if (uri === "file:///docs/readme") {
    const content = await fs.readFile("README.md", "utf-8");
    return {
      contents: [
        {
          uri: uri,
          mimeType: "text/markdown",
          text: content
        }
      ]
    };
  }

  throw new Error(`Unknown resource: ${uri}`);
});
```

### Resource Template

```typescript
import { ListResourceTemplatesRequestSchema } from "@modelcontextprotocol/sdk/types.js";

// List templates
server.setRequestHandler(ListResourceTemplatesRequestSchema, async () => ({
  resourceTemplates: [
    {
      uriTemplate: "file:///{path}",
      name: "Project File",
      description: "Read any file from project directory",
      mimeType: "text/plain"
    }
  ]
}));

// Read with template
server.setRequestHandler(ReadResourceRequestSchema, async (request) => {
  const uri = request.params.uri;

  // Parse template URI
  const match = uri.match(/^file:\/\/\/(.+)$/);
  if (match) {
    const path = match[1];
    const content = await fs.readFile(path, "utf-8");
    return {
      contents: [
        {
          uri: uri,
          mimeType: getMimeType(path),
          text: content
        }
      ]
    };
  }

  throw new Error(`Unknown resource: ${uri}`);
});

function getMimeType(path: string): string {
  if (path.endsWith(".md")) return "text/markdown";
  if (path.endsWith(".json")) return "application/json";
  if (path.endsWith(".py")) return "text/x-python";
  return "text/plain";
}
```

## Resource URI Patterns

### File System

```
file:///path/to/file.txt
file:///project/src/main.py
file:///docs/{category}/{page}.md
```

### Databases

```
database://users/table
database://products/{id}
database://analytics/query/{query_name}
```

### APIs

```
api://github/repos/{owner}/{repo}
api://weather/forecast/{city}
api://calendar/events/{date}
```

### Custom Schemas

```
travel://activities/{city}/{category}
docs://section/{topic}
config://settings/{key}
```

## Resource Metadata

### MIME Types

Specify appropriate MIME types for content:

```python
# Text formats
"text/plain"
"text/markdown"
"text/html"
"text/csv"

# Code
"text/x-python"
"text/javascript"
"application/json"

# Documents
"application/pdf"
"application/xml"

# Binary
"application/octet-stream"
"image/png"
"image/jpeg"
```

### Resource Description

Provide clear, helpful descriptions:

```python
@mcp.resource("github://repos/{owner}/{repo}/issues")
async def get_issues(owner: str, repo: str) -> str:
    """List all open issues in a GitHub repository.

    Returns issue titles, numbers, and creation dates.
    Only fetches open issues, not closed or merged ones.

    Args:
        owner: Repository owner username
        repo: Repository name
    """
```

## Resource Updates

### Subscribe to Changes

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("watch-server")

@mcp.resource("file:///logs/app.log")
async def get_app_log() -> str:
    """Get application log file."""
    with open("/var/log/app.log", "r") as f:
        return f.read()

# Notify clients when resource changes
async def watch_log_file():
    """Watch log file for changes."""
    last_modified = 0
    while True:
        current_modified = os.path.getmtime("/var/log/app.log")
        if current_modified > last_modified:
            # Notify subscribed clients
            await mcp.notify_resource_updated("file:///logs/app.log")
            last_modified = current_modified
        await asyncio.sleep(1)
```

## Best Practices

### 1. Consistent URI Schemes

Use consistent, descriptive URI patterns:

✅ Good:
```
file:///docs/readme.md
file:///src/main.py
database://users/profile/{id}
api://github/repos/{owner}/{repo}
```

❌ Bad:
```
readme.md
file123
db/users
gh/repo
```

### 2. Granular Resources

Provide specific, focused resources:

```python
# Good - specific resources
@mcp.resource("database://users/count")
async def get_user_count(): ...

@mcp.resource("database://users/active")
async def get_active_users(): ...

@mcp.resource("database://users/{id}")
async def get_user(id: str): ...

# Avoid - overly broad
@mcp.resource("database://everything")
async def get_everything(): ...
```

### 3. Efficient Data Loading

Load only what's needed:

```python
@mcp.resource("logs://app/{date}")
async def get_logs(date: str) -> str:
    """Get logs for specific date."""
    # Don't load all logs
    log_file = f"/var/log/app-{date}.log"

    # Read only last 1000 lines if file is large
    with open(log_file, "r") as f:
        lines = f.readlines()
        return "".join(lines[-1000:])
```

### 4. Error Handling

Handle missing resources gracefully:

```python
@mcp.resource("file:///{path}")
async def get_file(path: str) -> str:
    """Read project file."""
    file_path = Path(path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"File not found: {path}\n"
            f"Available files: {list_available_files()}"
        )

    if not file_path.is_file():
        raise ValueError(f"Not a file: {path}")

    if file_path.stat().st_size > 10_000_000:  # 10MB
        raise ValueError(f"File too large: {path}")

    return file_path.read_text()
```

### 5. Security

Validate paths and prevent directory traversal:

```python
import os

@mcp.resource("file:///{path}")
async def get_file(path: str) -> str:
    """Read file securely."""
    # Resolve absolute path
    base_dir = Path("/allowed/directory").resolve()
    requested_path = (base_dir / path).resolve()

    # Ensure path is within allowed directory
    if not str(requested_path).startswith(str(base_dir)):
        raise PermissionError(
            f"Access denied: {path} is outside allowed directory"
        )

    return requested_path.read_text()
```

### 6. Caching

Cache expensive operations:

```python
from functools import lru_cache
from datetime import datetime, timedelta

@lru_cache(maxsize=100)
async def fetch_github_data(owner: str, repo: str):
    """Fetch and cache GitHub data."""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.github.com/repos/{owner}/{repo}"
        )
        return response.json()

@mcp.resource("github://repos/{owner}/{repo}")
async def get_repo_info(owner: str, repo: str) -> str:
    """Get GitHub repository information."""
    data = await fetch_github_data(owner, repo)
    return json.dumps(data, indent=2)
```

## Parameter Completion

Provide suggestions for template parameters:

```python
@mcp.resource("travel://activities/{city}/{category}")
async def get_activities(city: str, category: str) -> str:
    """Get activities in a city by category."""
    return await fetch_activities(city, category)

# Provide completion hints
@mcp.completion("travel://activities/{city}/{category}")
async def complete_travel_params(partial: str, param: str):
    """Suggest parameter values."""
    if param == "city":
        cities = ["paris", "london", "tokyo", "new-york"]
        return [c for c in cities if c.startswith(partial.lower())]

    if param == "category":
        categories = ["museums", "restaurants", "parks", "monuments"]
        return [c for c in categories if c.startswith(partial.lower())]

    return []
```

## Testing Resources

Test resource implementations:

```python
# test_resources.py
import asyncio
from server import get_file, get_github_readme

async def test_resources():
    # Test direct resource
    content = await get_file("README.md")
    assert len(content) > 0

    # Test template resource
    readme = await get_github_readme("anthropics", "anthropic-sdk-python")
    assert "Anthropic" in readme

asyncio.run(test_resources())
```

## Multi-Server Integration

Resources from different servers combine seamlessly:

```
Server 1: File Server
├── file:///docs/readme.md
└── file:///src/{path}

Server 2: Database Server
├── database://users/{id}
└── database://analytics/report/{date}

Server 3: API Server
├── api://github/repos/{owner}/{repo}
└── api://weather/forecast/{city}

→ Claude can access all resources across servers
```

## Next Steps

See other reference files for:
- **tools.md**: Implementing executable tools
- **prompts.md**: Creating prompt templates
- **configuration.md**: Advanced configuration
