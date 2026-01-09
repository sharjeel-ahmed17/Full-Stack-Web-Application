# OpenAI Agents SDK - Handoffs

## Overview

Handoffs enable agents to delegate tasks to other specialized agents. The SDK represents handoffs as tools, appearing as `transfer_to_<agent_name>` functions to the LLM.

## Basic Handoffs

### Simple Delegation

```python
from agents import Agent

# Create specialized agents
billing_agent = Agent(
    name="Billing Specialist",
    instructions="Handle billing inquiries and payment processing"
)

refund_agent = Agent(
    name="Refund Specialist",
    instructions="Process refund requests and handle returns"
)

# Create triage agent with handoffs
triage_agent = Agent(
    name="Customer Service",
    instructions="Route customer inquiries to the appropriate specialist",
    handoffs=[billing_agent, refund_agent]
)

# The triage agent can now transfer to billing or refund agents
result = await Runner.run(
    triage_agent,
    "I need help with my bill"
)
# Agent will call transfer_to_billing_specialist tool
```

## Customizing Handoffs

Use the `handoff()` function for advanced configuration:

```python
from agents import handoff

triage_agent = Agent(
    name="Triage",
    handoffs=[
        billing_agent,  # Simple handoff
        handoff(
            agent=refund_agent,
            tool_name_override="escalate_to_refunds",
            tool_description_override="Transfer to refund team for return processing"
        )
    ]
)
```

## Handoff with Input Data

Request specific data during handoff using Pydantic models:

```python
from pydantic import BaseModel
from agents import handoff, RunContextWrapper

class EscalationData(BaseModel):
    reason: str
    customer_id: str
    priority: str

async def on_escalation(ctx: RunContextWrapper, input_data: EscalationData):
    """Called when escalation handoff occurs."""
    print(f"Escalating customer {input_data.customer_id}")
    print(f"Reason: {input_data.reason}")
    print(f"Priority: {input_data.priority}")
    # Log to monitoring system, send notifications, etc.

supervisor_agent = Agent(
    name="Supervisor",
    instructions="Handle escalated customer issues"
)

agent = Agent(
    name="Support Agent",
    handoffs=[
        handoff(
            agent=supervisor_agent,
            input_type=EscalationData,
            on_handoff=on_escalation
        )
    ]
)
```

## Conversation History Filtering

Control what conversation history is passed to the next agent:

```python
from agents import HandoffInputData, handoff_filters

# Remove all tool calls from history
specialist = Agent(
    name="Specialist",
    instructions="Handle specialized requests"
)

agent = Agent(
    name="Main Agent",
    handoffs=[
        handoff(
            agent=specialist,
            input_filter=handoff_filters.remove_all_tools
        )
    ]
)
```

### Custom Input Filter

```python
def custom_filter(input_data: HandoffInputData) -> HandoffInputData:
    """Remove sensitive information from history."""
    filtered_messages = []
    for msg in input_data.messages:
        # Filter out messages containing "password"
        if "password" not in msg.content.lower():
            filtered_messages.append(msg)

    return HandoffInputData(
        messages=filtered_messages,
        input=input_data.input
    )

agent = Agent(
    name="Agent",
    handoffs=[
        handoff(
            agent=secure_agent,
            input_filter=custom_filter
        )
    ]
)
```

## Conditional Handoffs

Enable or disable handoffs dynamically:

```python
from agents import RunContextWrapper

def is_business_hours(ctx: RunContextWrapper) -> bool:
    """Check if within business hours."""
    from datetime import datetime
    hour = datetime.now().hour
    return 9 <= hour < 17

human_agent = Agent(
    name="Human Support",
    instructions="Provide human assistance"
)

agent = Agent(
    name="Bot",
    handoffs=[
        handoff(
            agent=human_agent,
            is_enabled=is_business_hours  # Only available during business hours
        )
    ]
)
```

### Static Enabling/Disabling

```python
# Temporarily disable handoff
agent = Agent(
    name="Agent",
    handoffs=[
        handoff(
            agent=specialist,
            is_enabled=False  # Handoff disabled
        )
    ]
)
```

## Multi-Level Handoffs

Agents can hand off to agents that also have handoffs:

```python
# Level 3: Technical specialists
hardware_expert = Agent(
    name="Hardware Expert",
    instructions="Solve hardware issues"
)

software_expert = Agent(
    name="Software Expert",
    instructions="Solve software issues"
)

# Level 2: Technical support
tech_support = Agent(
    name="Technical Support",
    instructions="Handle technical issues, delegate to specialists if needed",
    handoffs=[hardware_expert, software_expert]
)

# Level 1: Front-line agent
frontline = Agent(
    name="Customer Service",
    instructions="Handle customer inquiries, escalate to tech support for technical issues",
    handoffs=[tech_support, billing_agent]
)

# Customer → Frontline → Tech Support → Hardware Expert (3-level handoff)
```

## Handoff Callbacks

Monitor and log handoff events:

```python
async def log_handoff(ctx: RunContextWrapper, input_data: dict):
    """Log all handoff events."""
    print(f"Handoff from: {ctx.agent.name}")
    print(f"Session: {ctx.session.session_id if ctx.session else 'None'}")
    print(f"Timestamp: {datetime.now()}")
    # Log to database, analytics, etc.

agent = Agent(
    name="Agent",
    handoffs=[
        handoff(
            agent=specialist,
            on_handoff=log_handoff
        )
    ]
)
```

## Recommended Handoff Prompts

Use recommended prompt prefix for better handoff understanding:

```python
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX

agent = Agent(
    name="Router",
    instructions=f"{RECOMMENDED_PROMPT_PREFIX}\n\nRoute customer requests to specialists",
    handoffs=[billing_agent, technical_agent, sales_agent]
)
```

The prefix includes guidance like:
- How to recognize when to hand off
- How to transfer context effectively
- When to handle requests directly vs delegate

## Handoff Return Values

Handoffs return control to the originating agent after completion:

```python
# Agent A hands off to Agent B
# Agent B completes task and returns result
# Agent A receives result and can continue

result = await Runner.run(main_agent, "Complex multi-step request")

# Check if handoff occurred
if result.handoff:
    print(f"Task delegated to: {result.handoff.agent.name}")
else:
    print("Task handled directly")
```

## Best Practices

### 1. Clear Specialization

Define clear boundaries for each agent:

```python
billing_agent = Agent(
    name="Billing",
    instructions="""
    Handle ONLY billing inquiries:
    - Payment processing
    - Invoice questions
    - Billing disputes

    DO NOT handle: refunds, technical support, sales
    """
)
```

### 2. Use Handoff Prompts

Include the recommended prompt prefix for routing agents.

### 3. Filter Sensitive Data

Use input filters to remove sensitive information before handoff.

### 4. Monitor Handoffs

Implement `on_handoff` callbacks for logging and monitoring.

### 5. Limit Handoff Depth

Avoid excessive handoff chains (3 levels max recommended).

### 6. Validate Input Data

Use Pydantic models for type-safe handoff inputs.

### 7. Business Hours Logic

Use conditional enabling for availability-based routing.

## Multi-Agent Orchestration Pattern

```python
# Specialized agents
researcher = Agent(
    name="Researcher",
    instructions="Research topics and gather information"
)

writer = Agent(
    name="Writer",
    instructions="Write content based on research"
)

editor = Agent(
    name="Editor",
    instructions="Edit and refine written content"
)

# Orchestrator agent
orchestrator = Agent(
    name="Content Pipeline",
    instructions="""
    Coordinate content creation:
    1. Use researcher to gather information
    2. Use writer to create content
    3. Use editor to refine final output
    """,
    handoffs=[researcher, writer, editor]
)

result = await Runner.run(
    orchestrator,
    "Create an article about AI agents"
)
# Orchestrator will coordinate the multi-step workflow
```

## Handoff vs Agent-as-Tool

**Use handoffs when:**
- You want to transfer control to another agent
- The specialist agent should handle the complete interaction
- You need the specialist's full context and capabilities

**Use agent-as-tool when:**
- You want to call an agent as a function
- You need the result back immediately
- The parent agent remains in control

```python
# Handoff: Transfer control
agent = Agent(
    name="Agent",
    handoffs=[specialist]  # User interacts with specialist
)

# Agent-as-Tool: Use as function
agent = Agent(
    name="Agent",
    tools=[specialist.as_tool()]  # Agent calls specialist internally
)
```
