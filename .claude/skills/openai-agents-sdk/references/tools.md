# OpenAI Agents SDK - Tools Reference

## Tool Types

The SDK supports three classes of tools:

1. **Hosted tools** - Run on OpenAI servers
2. **Function tools** - Python functions converted to tools
3. **Agent tools** - Agents used as tools by other agents

## Function Tools

### Basic Function Tool

```python
from agents import function_tool

@function_tool
async def search_database(query: str, limit: int = 10) -> list:
    """Search the database for matching records.

    Args:
        query: Search query string
        limit: Maximum number of results to return (default: 10)

    Returns:
        List of matching records
    """
    # Implementation
    results = []  # Query database
    return results
```

### Tool Naming and Description

- **Name**: Derived from function name (customize with `name_override`)
- **Description**: Extracted from docstring
- **Parameters**: Automatically generated from type annotations

```python
@function_tool(name_override="db_search")
async def search_database(query: str) -> list:
    """Custom tool name example."""
    pass
```

### Sync vs Async Functions

Both synchronous and asynchronous functions are supported:

```python
# Async function (preferred for I/O operations)
@function_tool
async def fetch_data(url: str) -> dict:
    """Fetch data from URL."""
    # Use async HTTP client
    return {}

# Sync function (for CPU-bound operations)
@function_tool
def calculate_hash(data: str) -> str:
    """Calculate hash of data."""
    import hashlib
    return hashlib.sha256(data.encode()).hexdigest()
```

### Type Annotations and Schema Generation

The SDK uses Python type annotations to generate JSON schemas:

```python
from typing import Optional, Literal
from pydantic import BaseModel

class Location(BaseModel):
    city: str
    country: str
    coordinates: Optional[tuple[float, float]] = None

@function_tool
async def get_weather(
    location: Location,
    units: Literal["celsius", "fahrenheit"] = "celsius",
    include_forecast: bool = False
) -> dict:
    """Fetch weather with detailed location."""
    return {
        "temperature": 22,
        "units": units,
        "forecast": [] if include_forecast else None
    }
```

### Multiple Return Types

Return different content types from tools:

```python
from agents import ToolOutputText, ToolOutputImage, ToolOutputFileContent

@function_tool
async def generate_report(format: str) -> ToolOutputText | ToolOutputImage:
    """Generate report in specified format."""
    if format == "text":
        return ToolOutputText(text="# Report\n\nData here...")
    elif format == "image":
        return ToolOutputImage(
            image_data=b"...",  # Image bytes
            mime_type="image/png"
        )
```

### Run Context Access

Access execution context within tools:

```python
from agents import RunContextWrapper

@function_tool
async def context_aware_tool(
    query: str,
    ctx: RunContextWrapper
) -> str:
    """Tool that accesses run context."""
    # Access agent information
    agent_name = ctx.agent.name

    # Access session if available
    session_id = ctx.session.session_id if ctx.session else None

    # Access custom user data
    user_data = ctx.user_data

    return f"Query: {query}, Agent: {agent_name}, Session: {session_id}"
```

### Error Handling in Tools

```python
from agents import function_tool

@function_tool(failure_error_function=lambda e: f"Tool failed: {str(e)}")
async def risky_operation(data: str) -> str:
    """Operation that might fail."""
    if not data:
        raise ValueError("Data cannot be empty")
    return f"Processed: {data}"

# Re-raise errors for custom handling
@function_tool(failure_error_function=None)
async def strict_operation(data: str) -> str:
    """Operation with strict error handling."""
    # Errors will propagate to caller
    return process_data(data)
```

### Conditional Tool Enabling

Control tool availability dynamically:

```python
from agents import function_tool, RunContextWrapper

def is_premium_user(ctx: RunContextWrapper) -> bool:
    """Check if user has premium access."""
    return ctx.user_data.get("premium", False)

@function_tool(is_enabled=is_premium_user)
async def premium_feature(query: str) -> str:
    """Feature only available to premium users."""
    return "Premium result"

# Static enabling/disabling
@function_tool(is_enabled=False)
async def disabled_tool() -> str:
    """This tool is currently disabled."""
    pass
```

## Hosted Tools

Tools that run on OpenAI's infrastructure:

```python
from agents import Agent, WebSearchTool, FileSearchTool, CodeInterpreterTool

agent = Agent(
    name="Research Assistant",
    instructions="Help with research and data analysis",
    tools=[
        WebSearchTool(),
        FileSearchTool(),
        CodeInterpreterTool()
    ]
)
```

### Available Hosted Tools

- **WebSearchTool** - Search the web for information
- **FileSearchTool** - Search uploaded files
- **ComputerTool** - Interact with computer environment
- **CodeInterpreterTool** - Execute Python code
- **HostedMCPTool** - Access MCP servers via OpenAI
- **ImageGenerationTool** - Generate images
- **LocalShellTool** - Execute shell commands

## Agents as Tools

Convert agents into tools for delegation:

```python
# Create specialized agent
spanish_translator = Agent(
    name="Spanish Translator",
    instructions="Translate English to Spanish"
)

# Use agent as a tool
orchestrator = Agent(
    name="Orchestrator",
    instructions="Help users with various tasks",
    tools=[
        spanish_translator.as_tool(
            tool_name="translate_to_spanish",
            tool_description="Translate text to Spanish"
        )
    ]
)
```

### Custom Output Extraction

Transform agent output before returning:

```python
def extract_translation(result: RunResult) -> str:
    """Extract only the translated text."""
    return result.final_output.strip()

spanish_tool = spanish_translator.as_tool(
    tool_name="translate",
    custom_output_extractor=extract_translation
)
```

### Streaming Nested Agents

Monitor nested agent execution:

```python
async def on_nested_stream(event):
    """Handle streaming events from nested agent."""
    if event.type == "text_delta":
        print(f"Nested: {event.data.delta}")

spanish_tool = spanish_translator.as_tool(
    tool_name="translate",
    on_stream=on_nested_stream
)
```

## Manual Tool Creation

For advanced use cases, manually create tools:

```python
from agents import FunctionTool

async def invoke_custom_tool(params: dict, ctx: RunContextWrapper) -> str:
    """Custom tool invocation logic."""
    query = params.get("query")
    return f"Processed: {query}"

custom_tool = FunctionTool(
    name="custom_search",
    description="Custom search tool",
    params_json_schema={
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "Search query"}
        },
        "required": ["query"]
    },
    on_invoke_tool=invoke_custom_tool
)
```

## Best Practices

1. **Clear Docstrings**: Include comprehensive descriptions and argument docs
2. **Type Annotations**: Always use type hints for automatic schema generation
3. **Error Handling**: Implement proper error handling with `failure_error_function`
4. **Async for I/O**: Use async functions for network/database operations
5. **Conditional Enabling**: Use feature flags to control tool availability
6. **Context Awareness**: Leverage `RunContextWrapper` for user-specific behavior
7. **Return Types**: Use specific return types (`ToolOutputText`, etc.) when needed
