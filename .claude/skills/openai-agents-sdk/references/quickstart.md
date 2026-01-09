# OpenAI Agents SDK - Quick Start

## Basic Agent Creation

```python
from agents import Agent, Runner

# Create a simple agent
agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant"
)

# Run synchronously
result = Runner.run_sync(agent, "Write a haiku about recursion.")
print(result.final_output)

# Run asynchronously
result = await Runner.run(agent, "Write a haiku about recursion.")
```

## Adding Tools to Agents

### Function Tool Decorator

```python
from agents import function_tool

@function_tool
async def fetch_weather(location: str, units: str = "celsius") -> str:
    """Fetch the weather for a given location.

    Args:
        location: The city name or coordinates
        units: Temperature units (celsius or fahrenheit)
    """
    # Implementation here
    return f"Weather in {location}: 22°{units[0].upper()}"

# Add tool to agent
agent = Agent(
    name="Weather Assistant",
    instructions="Help users with weather information",
    tools=[fetch_weather]
)
```

## Session Management

### Automatic Sessions

```python
from agents import Runner, SQLiteSession

# Create session (conversation history stored automatically)
session = SQLiteSession(session_id="user_123", db_path="sessions.db")

# First turn
result1 = await Runner.run(
    agent,
    "My name is Alice",
    session=session
)

# Second turn (agent remembers previous context)
result2 = await Runner.run(
    agent,
    "What's my name?",
    session=session
)
# Agent will respond: "Your name is Alice"
```

### Manual History Management

```python
# First turn
result1 = await Runner.run(agent, "My name is Alice")

# Build conversation history manually
conversation_history = result1.to_input_list()
conversation_history.append({"role": "user", "content": "What's my name?"})

# Second turn with manual history
result2 = await Runner.run(agent, conversation_history)
```

## Streaming Results

```python
from agents import Runner

result = Runner.run_streamed(agent, "Tell me a story")

async for event in result.stream:
    if event.type == "text_delta":
        print(event.data.delta, end="", flush=True)

# Access final result
print(f"\n\nFinal output: {result.final_output}")
```

## Common Patterns

### Agent with Multiple Tools

```python
@function_tool
async def get_user_info(user_id: str) -> dict:
    """Fetch user information."""
    return {"id": user_id, "name": "Alice", "email": "alice@example.com"}

@function_tool
async def send_email(to: str, subject: str, body: str) -> str:
    """Send an email."""
    return f"Email sent to {to}"

agent = Agent(
    name="Support Agent",
    instructions="Help users with their accounts and send emails",
    tools=[get_user_info, send_email]
)
```

### Error Handling

```python
from agents.exceptions import MaxTurnsExceeded, ModelBehaviorError

try:
    result = await Runner.run(
        agent,
        "Process this request",
        max_turns=10
    )
except MaxTurnsExceeded:
    print("Agent exceeded maximum turns")
except ModelBehaviorError as e:
    print(f"Model produced malformed output: {e}")
```

## Configuration

### RunConfig for Global Settings

```python
from agents import RunConfig

config = RunConfig(
    model="gpt-4o",
    max_turns=20,
    temperature=0.7
)

result = await Runner.run(
    agent,
    "Your request",
    config=config
)
```
