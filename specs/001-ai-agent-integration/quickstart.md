# Quickstart: AI Agent Integration

## Overview
This guide helps you get started with the AI Agent Integration feature that enables natural language task management through OpenAI Agents SDK connected to MCP tools.

## Prerequisites
- Python 3.13+ installed
- PostgreSQL database (Neon Serverless recommended)
- OpenAI API key
- MCP server from Spec 4.1 running

## Setup

### 1. Environment Variables
Create a `.env` file in the backend directory:
```bash
OPENAI_API_KEY=your_openai_api_key_here
DATABASE_URL=postgresql://username:password@localhost/dbname
MCP_SERVER_URL=http://localhost:8080  # Your MCP server endpoint
BETTER_AUTH_SECRET=your_auth_secret
```

### 2. Install Dependencies
```bash
cd backend
uv pip install openai-agents mcp sqlmodel fastapi
```

### 3. Database Migration
```bash
# Run existing migrations plus new AI agent models
alembic upgrade head
```

## Running the Service

### 1. Start MCP Server
Ensure your MCP server from Spec 4.1 is running:
```bash
# From your MCP server directory
python -m mcp_server.main
```

### 2. Start AI Agent Service
```bash
cd backend
python -m src.api.ai_agents
```

## Usage Examples

### Interacting with the AI Agent
Once the service is running, you can interact with the AI agent using natural language:

```
User: "Add a task to buy groceries"
AI: "I've created a task 'buy groceries' for you."

User: "Show me my pending tasks"
AI: "Here are your pending tasks: buy groceries, complete project proposal"

User: "Mark the grocery task as complete"
AI: "I've marked 'buy groceries' as complete."
```

### API Endpoints
- POST `/api/v1/ai-agent/chat` - Send messages to the AI agent
- GET `/api/v1/conversations/{conversation_id}` - Retrieve conversation history
- POST `/api/v1/conversations` - Start a new conversation

## Testing

### Unit Tests
```bash
pytest tests/unit/test_ai_agent.py
```

### Integration Tests
```bash
pytest tests/integration/test_mcp_integration.py
```

### AI Agent Specific Tests
```bash
pytest tests/ai_agent/
```

## Architecture Overview

```
[User] → [AI Agent Endpoint] → [OpenAI Agents SDK] → [MCP Tools] → [Task Management]
                                    ↓
                            [Conversation State] ↔ [PostgreSQL DB]
```

The system maintains statelessness while preserving conversation context through database persistence.