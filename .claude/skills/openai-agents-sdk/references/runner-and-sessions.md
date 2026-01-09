# OpenAI Agents SDK - Runner and Sessions

## Runner API

The `Runner` class executes agents with three modes: async, sync, and streaming.

### Async Execution (Primary Method)

```python
from agents import Agent, Runner

agent = Agent(name="Assistant", instructions="You are helpful")

# Async execution
result = await Runner.run(agent, "What is 2+2?")
print(result.final_output)
```

### Sync Execution

For non-async codebases:

```python
# Sync wrapper (delegates to async internally)
result = Runner.run_sync(agent, "What is 2+2?")
print(result.final_output)
```

### Streaming Execution

For real-time event delivery:

```python
# Returns RunResultStreaming
result = Runner.run_streamed(agent, "Tell me a long story")

# Stream events as they arrive
async for event in result.stream:
    if event.type == "text_delta":
        print(event.data.delta, end="", flush=True)
    elif event.type == "tool_call_start":
        print(f"\n[Tool: {event.data.tool_name}]")
    elif event.type == "tool_call_end":
        print(f"[Tool complete: {event.data.tool_name}]")

# Access final result after streaming
print(f"\n\nFinal: {result.final_output}")
```

## Result Objects

### RunResult

Contains comprehensive run information:

```python
result = await Runner.run(agent, "Hello")

# Access output
print(result.final_output)  # Final agent response

# Access conversation history
for message in result.messages:
    print(f"{message.role}: {message.content}")

# Check if agent handed off
if result.handoff:
    print(f"Handed off to: {result.handoff.agent.name}")

# Metadata
print(f"Turns: {result.turn_count}")
print(f"Model: {result.model}")
```

### Converting to Input List

Extract conversation state for manual history management:

```python
# First turn
result1 = await Runner.run(agent, "My name is Alice")

# Convert to input list
history = result1.to_input_list()
# Returns: [{"role": "user", "content": "My name is Alice"}, ...]

# Add new message
history.append({"role": "user", "content": "What's my name?"})

# Second turn with history
result2 = await Runner.run(agent, history)
```

## Session Management

Sessions automatically manage conversation history across multiple turns.

### SQLite Session

Store conversations in SQLite database:

```python
from agents import SQLiteSession, Runner

# Create session
session = SQLiteSession(
    session_id="user_123",
    db_path="conversations.db"
)

# First turn - history saved automatically
result1 = await Runner.run(
    agent,
    "My favorite color is blue",
    session=session
)

# Second turn - history loaded automatically
result2 = await Runner.run(
    agent,
    "What's my favorite color?",
    session=session
)
# Agent remembers: "Your favorite color is blue"
```

### SQLAlchemy Session

For existing database infrastructure:

```python
from agents import SQLAlchemySession
from sqlalchemy import create_engine

# Create engine
engine = create_engine("postgresql://user:pass@localhost/db")

# Create session
session = SQLAlchemySession(
    session_id="user_456",
    engine=engine
)

result = await Runner.run(agent, "Hello", session=session)
```

### Encrypted Session

Store conversations with encryption:

```python
from agents import EncryptedSession

# Create encrypted session
session = EncryptedSession(
    session_id="user_789",
    db_path="secure.db",
    encryption_key=b"your-32-byte-key-here-padded..."
)

result = await Runner.run(agent, "Sensitive data", session=session)
```

### Session Configuration

```python
# Custom table name
session = SQLiteSession(
    session_id="user_123",
    db_path="conversations.db",
    table_name="custom_conversations"
)

# Session with metadata
session = SQLiteSession(
    session_id="user_123",
    db_path="conversations.db",
    metadata={"user_tier": "premium", "region": "us-west"}
)
```

## RunConfig - Global Settings

Configure model, limits, and behavior:

```python
from agents import RunConfig, Runner

config = RunConfig(
    model="gpt-4o",
    max_turns=15,
    temperature=0.7,
    top_p=0.9,
    max_tokens=2000
)

result = await Runner.run(
    agent,
    "Your request",
    config=config
)
```

### Conversation History Nesting

Control how prior conversation history is presented:

```python
from agents import ConversationHistoryNestingBehavior

config = RunConfig(
    # Collapse prior turns into summary blocks (default)
    conversation_history_nesting=ConversationHistoryNestingBehavior.COLLAPSE_PRIOR_TURNS
)

# Or show full history
config = RunConfig(
    conversation_history_nesting=ConversationHistoryNestingBehavior.SHOW_FULL_HISTORY
)
```

### Turn Limits

```python
from agents import MaxTurnsExceeded

config = RunConfig(max_turns=5)

try:
    result = await Runner.run(agent, "Complex task", config=config)
except MaxTurnsExceeded:
    print("Agent exceeded turn limit")
```

## Server-Managed Conversations

Use OpenAI's Conversations API:

```python
# Start new conversation
result1 = await Runner.run(
    agent,
    "Hello",
    conversation_id="conv_abc123"
)

# Continue conversation
result2 = await Runner.run(
    agent,
    "Follow-up question",
    conversation_id="conv_abc123"
)

# Or chain responses
result2 = await Runner.run(
    agent,
    "Follow-up",
    previous_response_id=result1.response_id
)
```

## Exception Handling

Handle common exceptions:

```python
from agents.exceptions import (
    MaxTurnsExceeded,
    ModelBehaviorError,
    UserError,
    InputGuardrailTripwireTriggered,
    OutputGuardrailTripwireTriggered
)

try:
    result = await Runner.run(agent, "Request")
except MaxTurnsExceeded:
    print("Agent exceeded maximum turns")
except ModelBehaviorError as e:
    print(f"Model produced malformed output: {e}")
except UserError as e:
    print(f"API misuse: {e}")
except InputGuardrailTripwireTriggered as e:
    print(f"Input blocked by guardrail: {e}")
except OutputGuardrailTripwireTriggered as e:
    print(f"Output blocked by guardrail: {e}")
```

## Execution Loop

The Runner operates through this loop:

1. Call the LLM with current context
2. Process response:
   - **Final response**: Return result
   - **Tool calls**: Execute tools, continue
   - **Handoff**: Transfer to another agent
3. Repeat until completion or `max_turns` reached

## Streaming Events

Available event types when streaming:

```python
result = Runner.run_streamed(agent, "Query")

async for event in result.stream:
    match event.type:
        case "text_delta":
            # Incremental text output
            print(event.data.delta, end="")
        case "tool_call_start":
            # Tool invocation began
            print(f"\nCalling: {event.data.tool_name}")
        case "tool_call_end":
            # Tool completed
            print(f"Result: {event.data.result}")
        case "handoff":
            # Agent handed off to another
            print(f"Handoff to: {event.data.agent.name}")
        case "turn_complete":
            # Single turn finished
            print("Turn complete")
```

## Manual History Management Pattern

When not using sessions:

```python
# Start conversation
result1 = await Runner.run(agent, "First message")

# Build history
conversation = result1.to_input_list()

# Add new user message
conversation.append({
    "role": "user",
    "content": "Second message"
})

# Continue with history
result2 = await Runner.run(agent, conversation)

# Keep building
conversation = result2.to_input_list()
conversation.append({
    "role": "user",
    "content": "Third message"
})

result3 = await Runner.run(agent, conversation)
```

## Best Practices

1. **Use Sessions**: Prefer automatic session management over manual history
2. **Async First**: Use async execution for better concurrency
3. **Stream Long Responses**: Use streaming for real-time feedback
4. **Set Turn Limits**: Always configure `max_turns` to prevent infinite loops
5. **Handle Exceptions**: Catch and handle specific exceptions gracefully
6. **Secure Sessions**: Use `EncryptedSession` for sensitive data
7. **Database Sessions**: Use `SQLAlchemySession` for production databases
