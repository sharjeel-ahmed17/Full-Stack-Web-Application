# Quickstart: AI-Powered Todo Chatbot (Phase 3)

**Feature**: 002-ai-chatbot | **Date**: 2025-12-26 | **Phase**: 1 (Design)

## Overview

This guide helps developers set up and run the Phase 3 AI Chatbot feature locally. It assumes Phase 2 (Task CRUD + Auth) is already working.

## Prerequisites

- Phase 2 backend and frontend running successfully
- Python 3.13+ installed
- Node.js 18+ and npm/pnpm installed
- PostgreSQL database accessible (Neon Serverless or local Docker container)
- OpenAI API key (obtain from [platform.openai.com](https://platform.openai.com))

---

## Backend Setup

### 1. Install Phase 3 Dependencies

Navigate to the backend directory and install new packages:

```bash
cd backend

# Install OpenAI Agents SDK
pip install openai-agents

# Install MCP SDK
pip install mcp

# Verify installation
python -c "import openai_agents; import mcp; print('Dependencies installed successfully')"
```

### 2. Configure Environment Variables

Add the following to `backend/.env`:

```bash
# Existing Phase 2 variables (unchanged)
DATABASE_URL=postgresql://user:password@host:5432/dbname
BETTER_AUTH_SECRET=your-secret-key-here

# New Phase 3 variables
OPENAI_API_KEY=sk-proj-...your-openai-key-here
```

**Security Note**: Never commit `.env` file to version control. Ensure `.env` is in `.gitignore`.

### 3. Run Database Migration

Create and apply the migration for conversation and message models:

```bash
cd backend

# Generate migration (if not already created)
alembic revision --autogenerate -m "Add conversation and message models for AI chatbot"

# Apply migration
alembic upgrade head

# Verify tables were created
psql $DATABASE_URL -c "\dt conversations messages"
```

**Expected Output**:
```
              List of relations
 Schema |      Name       | Type  |  Owner
--------+-----------------+-------+----------
 public | conversations   | table | dbuser
 public | messages        | table | dbuser
```

### 4. Verify Backend Structure

Ensure the following files exist (created during implementation phase):

```
backend/src/
├── ai/
│   ├── __init__.py
│   ├── agent.py         # OpenAI agent configuration
│   └── prompts.py       # System prompts
├── mcp/
│   ├── __init__.py
│   ├── server.py        # MCP server initialization
│   └── tools/
│       ├── __init__.py
│       ├── add_task.py
│       ├── list_tasks.py
│       ├── update_task.py
│       ├── delete_task.py
│       └── complete_task.py
├── models/
│   ├── conversation.py  # NEW
│   └── message.py       # NEW
├── schemas/
│   └── chat.py          # NEW
├── services/
│   └── chat.py          # NEW
└── api/v1/
    └── chat.py          # NEW
```

### 5. Start Backend Server

```bash
cd backend
uvicorn src.main:app --reload --port 8000
```

**Verify Backend**:
- Open [http://localhost:8000/docs](http://localhost:8000/docs)
- Check for new endpoint: `POST /api/v1/chat`
- Verify OpenAPI schema includes chat endpoint

---

## Frontend Setup

### 1. Install Phase 3 Dependencies

Navigate to the frontend directory and install ChatKit:

```bash
cd frontend

# Install chat UI dependencies
npm install

# Verify installation
npm list
```

### 2. Verify Frontend Structure

Ensure the following files exist (created during implementation phase):

```
frontend/
├── app/
│   └── chat/
│       └── page.tsx     # NEW: Chat page route
├── components/
│   └── chat/
│       ├── ChatInterface.tsx  # NEW
│       └── MessageList.tsx    # NEW
└── lib/
    └── api.ts           # UPDATED: Add chatApi.sendMessage()
```

### 3. Start Frontend Server

```bash
cd frontend
npm run dev
```

**Verify Frontend**:
- Open [http://localhost:3000](http://localhost:3000)
- Navigate to `/chat` route
- Verify chat UI renders (even if not yet functional)

---

## Testing the Integration

### 1. Authenticate a Test User

If you don't have a test user yet:

```bash
# Create test user via API
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "testpass123"}'

# Login to get JWT token
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "testpass123"}'
```

**Expected Response**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 2. Test Chat API Directly (Backend)

Test the chat endpoint using curl:

```bash
# Replace <JWT_TOKEN> with the token from login
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"message": "Add buy groceries to my tasks"}'
```

**Expected Response**:
```json
{
  "message": "I've added 'buy groceries' to your tasks. Your task has been created successfully!",
  "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
  "timestamp": "2025-12-26T12:00:00Z"
}
```

### 3. Test Chat UI (Frontend)

1. Open [http://localhost:3000/chat](http://localhost:3000/chat)
2. Login with test credentials (test@example.com / testpass123)
3. Type: "Add buy milk to my tasks"
4. Verify:
   - Message appears in chat history
   - Assistant response confirms task creation
   - Task appears in `/tasks` page

### 4. Verify Task Operations via Chat

Test all MCP tools:

| User Message                        | Expected Tool Call      | Expected Result                          |
|-------------------------------------|-------------------------|------------------------------------------|
| "Add buy milk to my tasks"          | add_task                | Task created confirmation                |
| "What are my tasks?"                | list_tasks              | List of all tasks displayed              |
| "Mark buy milk as done"             | list_tasks, complete_task | Task marked complete                    |
| "Change buy milk to buy almond milk"| list_tasks, update_task | Task title updated                       |
| "Delete buy milk"                   | list_tasks, delete_task | Task deleted confirmation                |

### 5. Verify User Isolation (Security Test)

1. Create two test users (user1@test.com, user2@test.com)
2. Login as user1, add task "User 1 Task"
3. Login as user2, try to list tasks
4. Verify: user2 sees NO tasks from user1

---

## Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'openai_agents'`

**Solution**:
```bash
cd backend
pip install openai-agents
python -c "import openai_agents; print(openai_agents.__version__)"
```

### Issue: `ModuleNotFoundError: No module named 'mcp'`

**Solution**:
```bash
cd backend
pip install mcp
python -c "import mcp; print('MCP installed')"
```

### Issue: `401 Unauthorized` when calling `/api/v1/chat`

**Cause**: Missing or invalid JWT token

**Solution**:
1. Verify JWT token is included in `Authorization: Bearer <token>` header
2. Check token hasn't expired (default: 7 days)
3. Re-login to get a fresh token

### Issue: `500 Internal Server Error` when sending chat message

**Possible Causes**:
1. **Missing OPENAI_API_KEY**: Check `backend/.env` has `OPENAI_API_KEY` set
2. **OpenAI API Rate Limit**: Wait a few seconds and retry
3. **Database Connection Error**: Verify `DATABASE_URL` is correct and database is running

**Debug Steps**:
```bash
# Check backend logs
cd backend
tail -f logs/app.log

# Verify database connection
psql $DATABASE_URL -c "SELECT 1;"

# Test OpenAI API key
python -c "
import openai
openai.api_key = 'your-key-here'
print(openai.Model.list())
"
```

### Issue: Chat UI doesn't render

**Possible Causes**:
1. **Dependencies not installed**: Run `npm install` in frontend/
2. **TypeScript errors**: Check `npm run build` for errors
3. **Missing chat route**: Verify `frontend/app/chat/page.tsx` exists

**Debug Steps**:
```bash
cd frontend
npm run build
# Check for TypeScript errors in output
```

### Issue: Agent doesn't call MCP tools

**Possible Causes**:
1. **System prompt not strict enough**: Agent tries to answer without tools
2. **MCP server not registered**: Agent can't discover tools
3. **Tool schema invalid**: Agent can't parse tool definitions

**Debug Steps**:
```bash
# Check backend logs for MCP tool registration
cd backend
grep "MCP tool registered" logs/app.log

# Verify agent configuration
python -c "from src.ai.agent import agent; print(agent.tools)"
```

---

## API Documentation

### Chat API Endpoint

**Endpoint**: `POST /api/v1/chat`

**Headers**:
- `Authorization: Bearer <JWT_TOKEN>` (required)
- `Content-Type: application/json` (required)

**Request Body**:
```json
{
  "message": "Add buy groceries to my tasks",
  "conversation_id": "uuid-optional"
}
```

**Response** (200 OK):
```json
{
  "message": "I've added 'buy groceries' to your tasks!",
  "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
  "timestamp": "2025-12-26T12:00:00Z"
}
```

**Error Responses**:
- `401 Unauthorized`: Missing/invalid JWT token
- `403 Forbidden`: User not authorized for conversation
- `422 Validation Error`: Invalid request body
- `500 Internal Server Error`: Agent/database error

For full API specification, see [contracts/chat-api.openapi.yaml](./contracts/chat-api.openapi.yaml).

---

## Development Workflow

### 1. Run Backend + Frontend Concurrently

Use two terminal windows:

**Terminal 1 (Backend)**:
```bash
cd backend
uvicorn src.main:app --reload --port 8000
```

**Terminal 2 (Frontend)**:
```bash
cd frontend
npm run dev
```

### 2. Watch Backend Logs

```bash
cd backend
tail -f logs/app.log | grep "MCP\|CHAT\|ERROR"
```

### 3. Run Tests

**Backend Tests**:
```bash
cd backend
pytest tests/unit/mcp/
pytest tests/integration/api/test_chat.py
pytest tests/e2e/test_chat_flows.py
```

**Frontend Tests**:
```bash
cd frontend
npm run test:chat
```

### 4. Check Code Quality

**Backend Linting**:
```bash
cd backend
ruff check src/
mypy src/
```

**Frontend Linting**:
```bash
cd frontend
npm run lint
npm run type-check
```

---

## Environment Variables Reference

### Backend (.env)

```bash
# Database (Phase 2)
DATABASE_URL=postgresql://user:password@host:5432/dbname

# Authentication (Phase 2)
BETTER_AUTH_SECRET=your-secret-key-here

# OpenAI (Phase 3)
OPENAI_API_KEY=sk-proj-...your-key-here

# Optional: MCP Server Config (Phase 3)
MCP_SERVER_TRANSPORT=stdio  # Default: stdio
MCP_TOOL_TIMEOUT=30         # Seconds, default: 30
```

### Frontend (.env.local)

```bash
# API Base URL
NEXT_PUBLIC_API_URL=http://localhost:8000

# Optional: ChatKit Config
NEXT_PUBLIC_CHATKIT_STREAMING=true  # Enable response streaming
```

---

## Next Steps

After verifying local setup:

1. **Run Full Test Suite**: Ensure all Phase 3 tests pass
2. **Manual Testing**: Test all user stories from spec.md
3. **Performance Testing**: Verify <3s response time (spec SC-005)
4. **Security Testing**: Verify user isolation (spec SC-006)
5. **Integration Testing**: Verify Phase 2 unchanged (spec SC-007)

---

## Resources

- [OpenAI Agents SDK Documentation](https://openai.github.io/openai-agents-python/)
- [MCP Python SDK GitHub](https://github.com/modelcontextprotocol/python-sdk)
- [OpenAI ChatKit.js Documentation](https://openai.github.io/chatkit-js/)
- [Feature Specification](./spec.md)
- [Implementation Plan](./plan.md)
- [Data Model](./data-model.md)
- [API Contracts](./contracts/)

---

**Quickstart Last Updated**: 2025-12-26
**Author**: Claude Sonnet 4.5 (AI Agent)
