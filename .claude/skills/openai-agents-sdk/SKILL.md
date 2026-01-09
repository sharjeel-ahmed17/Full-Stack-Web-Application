---
name: openai-agents-sdk
description: Comprehensive guide for building AI agents with the OpenAI Agents SDK. Use when Claude needs to work with OpenAI agents for (1) creating agents with instructions and tools, (2) implementing function tools or hosted tools, (3) running agents with sessions and conversation history, (4) implementing multi-agent workflows with handoffs, (5) integrating MCP (Model Context Protocol) servers, (6) managing agent execution with Runner, (7) streaming agent responses, or any other OpenAI Agents SDK tasks.
license: Complete terms in LICENSE.txt
---

# OpenAI Agents SDK

## Overview

The OpenAI Agents SDK provides four fundamental primitives for building AI agent systems:

1. **Agents**: Language models equipped with instructions and tools
2. **Handoffs**: Enable delegation between agents for specialized tasks
3. **Guardrails**: Validate agent inputs and outputs
4. **Sessions**: Maintain conversation history across agent runs

This skill provides comprehensive guidance for building production-ready agent systems.

## Quick Navigation

Use the following reference files based on your needs:

- **Getting started**: See [quickstart.md](references/quickstart.md) for basic agent creation, tool usage, and session management
- **Tool development**: See [tools.md](references/tools.md) for function tools, hosted tools, and agents-as-tools
- **Execution and state**: See [runner-and-sessions.md](references/runner-and-sessions.md) for running agents, session management, and streaming
- **Multi-agent systems**: See [handoffs.md](references/handoffs.md) for agent delegation and orchestration patterns
- **External integrations**: See [mcp-integration.md](references/mcp-integration.md) for Model Context Protocol server integration

## Core Concepts

### Agents

Agents are LLMs configured with instructions and optional tools:

```python
from agents import Agent

agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant",
    tools=[...]  # Optional tools
)
```

### Tools

Three types of tools extend agent capabilities:

1. **Function tools**: Python functions decorated with `@function_tool`
2. **Hosted tools**: Tools running on OpenAI infrastructure (WebSearchTool, CodeInterpreterTool, etc.)
3. **Agent tools**: Other agents used as tools via `agent.as_tool()`

### Runner

Execute agents using the Runner class:

```python
from agents import Runner

# Synchronous
result = Runner.run_sync(agent, "Your message")

# Asynchronous
result = await Runner.run(agent, "Your message")

# Streaming
result = Runner.run_streamed(agent, "Your message")
```

### Sessions

Automatically manage conversation history across turns:

```python
from agents import SQLiteSession

session = SQLiteSession(session_id="user_123", db_path="conversations.db")
result = await Runner.run(agent, "Message", session=session)
```

## Common Workflows

### 1. Single Agent with Tools

**When to use**: Simple task automation, API integrations, data processing

**Reference**: [quickstart.md](references/quickstart.md), [tools.md](references/tools.md)

**Pattern**:
```python
@function_tool
async def my_tool(param: str) -> str:
    """Tool implementation."""
    return result

agent = Agent(
    name="Agent",
    instructions="Instructions here",
    tools=[my_tool]
)

result = await Runner.run(agent, "Task")
```

### 2. Conversational Agent with Memory

**When to use**: Chatbots, customer service, multi-turn interactions

**Reference**: [runner-and-sessions.md](references/runner-and-sessions.md)

**Pattern**:
```python
session = SQLiteSession(session_id=user_id, db_path="db.sqlite")

# Each turn automatically maintains context
result = await Runner.run(agent, message, session=session)
```

### 3. Multi-Agent Orchestration

**When to use**: Complex workflows, specialized domains, task routing

**Reference**: [handoffs.md](references/handoffs.md)

**Pattern**:
```python
specialist1 = Agent(name="Specialist1", instructions="...")
specialist2 = Agent(name="Specialist2", instructions="...")

orchestrator = Agent(
    name="Orchestrator",
    instructions="Route tasks to specialists",
    handoffs=[specialist1, specialist2]
)
```

### 4. External Tool Integration

**When to use**: Database access, API calls, file systems

**Reference**: [mcp-integration.md](references/mcp-integration.md)

**Pattern**:
```python
from agents import MCPServerStreamableHttp

mcp_server = MCPServerStreamableHttp(url="https://mcp.example.com")

agent = Agent(
    name="Agent",
    tools=[mcp_server]
)
```

## Decision Tree

Follow this tree to find the right approach:

```
Need to build an agent system?
│
├─ Single agent, simple tasks
│  └─> Use: Agent + function_tools
│     Reference: quickstart.md, tools.md
│
├─ Need conversation memory?
│  └─> Use: Sessions (SQLiteSession, SQLAlchemySession)
│     Reference: runner-and-sessions.md
│
├─ Multiple specialized agents?
│  ├─ Need delegation/routing?
│  │  └─> Use: Handoffs
│  │     Reference: handoffs.md
│  │
│  └─ Need to call agents as functions?
│     └─> Use: agent.as_tool()
│        Reference: tools.md
│
├─ Need external tools/services?
│  └─> Use: MCP integration
│     Reference: mcp-integration.md
│
└─ Need real-time updates?
   └─> Use: Runner.run_streamed()
      Reference: runner-and-sessions.md
```

## Best Practices

### Agent Design

1. **Clear Instructions**: Write specific, actionable instructions
2. **Tool Naming**: Use descriptive names that explain tool purpose
3. **Type Safety**: Always use type annotations for function tools
4. **Error Handling**: Implement proper error handling in tools
5. **Async for I/O**: Use async functions for network/database operations

### Session Management

1. **Use Sessions**: Prefer automatic session management over manual history
2. **Separate Sessions**: Use unique session IDs per user/conversation
3. **Secure Data**: Use `EncryptedSession` for sensitive conversations
4. **Database Sessions**: Use `SQLAlchemySession` for production databases

### Multi-Agent Systems

1. **Clear Boundaries**: Define clear responsibilities for each agent
2. **Limit Depth**: Avoid excessive handoff chains (3 levels max)
3. **Filter Context**: Use input filters to remove unnecessary data
4. **Monitor Handoffs**: Implement callbacks for logging and monitoring

### Performance

1. **Cache Tools**: Enable `cache_tools_list=True` for MCP servers
2. **Set Limits**: Configure `max_turns` to prevent infinite loops
3. **Stream Long Responses**: Use streaming for better user experience
4. **Connection Pooling**: Reuse database connections for sessions

## Example: Complete Agent System

```python
from agents import Agent, Runner, SQLiteSession, function_tool

# Define tools
@function_tool
async def search_database(query: str) -> list:
    """Search database for records."""
    # Implementation
    return []

@function_tool
async def send_notification(message: str) -> str:
    """Send notification to user."""
    # Implementation
    return "Sent"

# Create agent
agent = Agent(
    name="Support Agent",
    instructions="Help users with their requests using available tools",
    tools=[search_database, send_notification]
)

# Setup session
session = SQLiteSession(
    session_id="user_123",
    db_path="conversations.db"
)

# Run agent
result = await Runner.run(
    agent,
    "Find my recent orders",
    session=session
)

print(result.final_output)
```

## Troubleshooting

### Agent Not Using Tools

**Issue**: Agent responds without calling available tools

**Solutions**:
- Make tool descriptions more explicit
- Include usage examples in tool docstrings
- Adjust agent instructions to mention when to use tools

### Handoff Not Working

**Issue**: Agent not transferring to specialist

**Solutions**:
- Use `RECOMMENDED_PROMPT_PREFIX` from `agents.extensions.handoff_prompt`
- Make handoff descriptions clearer
- Check if handoff is conditionally disabled (`is_enabled=False`)

### Session Not Persisting

**Issue**: Conversation history not maintained

**Solutions**:
- Verify session ID is consistent across turns
- Check database permissions and path
- Ensure same session object is used

### MCP Server Connection Fails

**Issue**: Cannot connect to MCP server

**Solutions**:
- Verify server URL and accessibility
- Check authentication headers/tokens
- Enable retries with `max_retries` parameter
- Review server logs for errors

## Additional Resources

- **Official Documentation**: https://openai.github.io/openai-agents-python/
- **GitHub Repository**: https://github.com/openai/openai-agents-python
- **MCP Specification**: https://modelcontextprotocol.io/

## Reference Files

All reference files are located in the `references/` directory:

1. **quickstart.md** - Basic examples and common patterns (200 lines)
2. **tools.md** - Comprehensive tool development guide (300 lines)
3. **runner-and-sessions.md** - Execution and state management (280 lines)
4. **handoffs.md** - Multi-agent orchestration patterns (350 lines)
5. **mcp-integration.md** - External tool integration (340 lines)

Load reference files as needed based on the specific task requirements.
