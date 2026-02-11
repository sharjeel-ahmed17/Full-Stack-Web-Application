# Research: AI-Powered Todo Chatbot (Phase 3)

**Feature**: 002-ai-chatbot | **Date**: 2025-12-26 | **Phase**: 0 (Research)

## Purpose

Resolve all NEEDS CLARIFICATION items from the Technical Context section of plan.md before proceeding to Phase 1 design.

## Research Questions

### 1. OpenAI Agents SDK - Official Package and Setup

**Question**: What is the official OpenAI Agents SDK package for Python? How does it work with Python 3.13+? What's the basic setup pattern?

**Findings**:

- **Package Name**: `openai-agents` (PyPI)
- **Installation**: `pip install openai-agents`
- **Python Compatibility**: Requires Python 3.9 or newer ✅ Compatible with Python 3.13+
- **Current Version**: 0.6.4 (as of research date)
- **GitHub**: [github.com/openai/openai-agents-python](https://github.com/openai/openai-agents-python)
- **Documentation**: [openai.github.io/openai-agents-python/](https://openai.github.io/openai-agents-python/)

**Key Primitives**:
- **Agents**: LLMs equipped with instructions (system prompts) and tools
- **Handoffs**: Agents can delegate to other agents
- **Guardrails**: Validation of agent inputs and outputs
- **Sessions**: Automatic conversation history maintenance

**System Prompt Configuration**:
- Agents are created with custom instructions that define behavior
- Supports strict enforcement of tool-only behavior (no free-form responses outside of tool calls)

**Tool Calling**:
- Native integration with Chat Completions API and Responses API
- Works with OpenAI models and any provider with Chat Completions-style endpoint

**Decision**: Use `openai-agents` package. Suitable for Phase 3 requirements (Python 3.13+, FastAPI compatible, system prompt configuration, tool calling).

---

### 2. Official MCP SDK - Implementation Pattern

**Question**: What is the Official MCP SDK for Python? How do we define and register MCP tools within FastAPI? How does it connect to OpenAI agents?

**Findings**:

- **Package Name**: `mcp` (PyPI)
- **Installation**: `pip install mcp`
- **Current Version**: 1.25.0 (spec 2025-11-25)
- **GitHub**: [github.com/modelcontextprotocol/python-sdk](https://github.com/modelcontextprotocol/python-sdk)
- **Governance**: Donated to Agentic AI Foundation (AAIF) under Linux Foundation (Dec 2025) by Anthropic, Block, OpenAI, with support from Google, Microsoft, AWS, Cloudflare, Bloomberg

**SDK Components**:
- **High-level FastMCP server**: Quick development for exposing tools
- **Low-level server**: Full control over MCP protocol
- **Client interface**: Connect to MCP servers
- **Transports**: stdio, streamable HTTP

**MCP Capabilities**:
- **Tools**: Expose callable functions (add_task, list_tasks, etc.)
- **Resources**: Expose data
- **Prompts**: Define interaction patterns

**Integration with OpenAI Agents SDK**:
- OpenAI Agents SDK (as of March 2025) ships with **built-in MCP support**
- Import: `from agents.mcp import MCPServerStdio`
- OpenAI officially adopted MCP across ChatGPT desktop app, Agents SDK, and Responses API
- JSON-RPC bridge allows agents to discover and invoke tools from MCP servers
- Extension package available: [github.com/lastmile-ai/openai-agents-mcp](https://github.com/lastmile-ai/openai-agents-mcp)

**Integration Pattern**:
1. Define MCP server using FastMCP (high-level) or low-level server
2. Register tools (functions) in MCP server
3. Connect OpenAI agent to MCP server using `MCPServerStdio` or client interface
4. Agent discovers and calls tools via JSON-RPC

**Decision**: Use `mcp` package with FastMCP for quick tool registration. OpenAI Agents SDK has native MCP integration via `agents.mcp` module. MCP tools will wrap existing task service business logic (no direct database access by MCP layer).

**Sources**:
- [MCP Python SDK on PyPI](https://pypi.org/project/mcp/)
- [MCP Python SDK GitHub](https://github.com/modelcontextprotocol/python-sdk)
- [OpenAI Agents SDK MCP Documentation](https://openai.github.io/openai-agents-python/mcp/)
- [DigitalOcean: How to Use MCP with OpenAI Agents](https://www.digitalocean.com/community/tutorials/how-to-use-mcp-with-openai-agents)

---

### 3. ChatKit React - Package and Setup

**Question**: What is the official ChatKit React package for Next.js? How does it integrate with Next.js 16+ App Router?

**Findings**:

- **Package Name**: Custom chat UI components using React and Tailwind CSS
- **Alternative**: `@chatscope/chat-ui-kit-react` (Open source, general-purpose, version 2.1.1)
- **Documentation**: [openai.github.io/chatkit-js/](https://openai.github.io/chatkit-js/)
- **Python SDK**: ChatKit Python SDK available for backend integration

**OpenAI ChatKit Features**:
- Part of OpenAI's AgentKit
- React components and Web Components
- Response streaming
- File attachments
- Thread management
- Integration with OpenAI Agent Builder platform
- Can use OpenAI-hosted backend OR custom backend

**Next.js Integration**:
- Compatible with Next.js 15+ (and therefore 16+)
- Provides React hooks and components
- Can connect to custom API endpoint (`POST /api/v1/chat`)
- Implementation guide available: [Build with Matija - ChatKit Next.js Integration](https://www.buildwithmatija.com/blog/chatkit-nextjs-integration)

**Alternative (@chatscope/chat-ui-kit-react)**:
- Open source, mature (last published 7 months ago)
- General-purpose chat UI components
- No OpenAI-specific features
- More control, less opinionated

**Decision**: Use custom chat UI components for Phase 3. It aligns with the OpenAI Agents SDK choice, provides production-grade chat UI, and supports custom backend integration (required for our FastAPI `/api/v1/chat` endpoint).

**Sources**:
- [OpenAI ChatKit.js Documentation](https://openai.github.io/chatkit-js/)
- [Build with Matija: ChatKit Next.js Integration](https://www.buildwithmatija.com/blog/chatkit-nextjs-integration)
- [Chatscope React Chat UI Kit on npm](https://www.npmjs.com/package/@chatscope/chat-ui-kit-react)

---

## Architecture Decisions Summary

### Backend Architecture

**Selected Stack**:
- **AI Agent**: `openai-agents` (v0.6.4+) with Session management
- **MCP Layer**: `mcp` (v1.25.0+) with FastMCP for tool registration
- **Integration**: `from agents.mcp import MCPServerStdio` (native support in OpenAI Agents SDK)

**Tool Orchestration Pattern**:
```
User Message → POST /api/v1/chat
    ↓
Chat Service loads conversation history from PostgreSQL
    ↓
OpenAI Agent (with system prompt: "Use MCP tools only")
    ↓
Agent discovers tools from MCP Server (via JSON-RPC)
    ↓
Agent calls MCP tool (e.g., add_task) with user_id
    ↓
MCP tool delegates to Task Service (existing business logic)
    ↓
Task Service performs database operation (SQLModel)
    ↓
Result returned to Agent → formatted response → persisted to DB → returned to frontend
```

**Security Enforcement**:
- JWT validation at `/api/v1/chat` endpoint (existing auth middleware)
- All MCP tools require `user_id` parameter (extracted from JWT)
- MCP tools call Task Service with `user_id` filter (existing isolation logic)
- OpenAI API key stored backend-only (environment variable)

---

### Frontend Architecture

**Selected Stack**:
- **Chat UI**: Custom chat components with React and Tailwind CSS, with custom backend integration
- **API Client**: Custom type-safe client calling `POST /api/v1/chat`
- **Authentication**: JWT token attached automatically (existing Better Auth setup)

**UI Component Structure**:
```
app/chat/page.tsx (Chat page route)
    ↓
components/chat/ChatInterface.tsx (ChatKit wrapper)
    ↓
lib/api.ts → chatApi.sendMessage(message, jwt)
    ↓
POST /api/v1/chat (FastAPI backend)
```

---

## Alternatives Considered and Rejected

### Alternative 1: LangChain + Custom Tool Layer
**Rejected Because**:
- OpenAI Agents SDK is lighter weight and better aligned with OpenAI models
- MCP is an emerging open standard with broader ecosystem support (Linux Foundation governance)
- LangChain abstractions introduce unnecessary complexity for this use case

### Alternative 2: Direct OpenAI API (no Agents SDK)
**Rejected Because**:
- Would require manual session/conversation history management
- No built-in MCP integration
- More boilerplate for tool calling and error handling

### Alternative 3: @chatscope/chat-ui-kit-react (frontend)
**Rejected Because**:
- OpenAI ChatKit provides better integration with OpenAI Agents SDK
- ChatKit has streaming and thread management built-in
- ChatKit is production-grade and actively maintained by OpenAI

---

## Best Practices

### MCP Tool Implementation
1. **Reuse Existing Business Logic**: MCP tools MUST delegate to Task Service, never access database directly
2. **User Context Required**: Every MCP tool MUST accept `user_id` parameter
3. **Error Handling**: MCP tools MUST return structured errors (no stack traces to agent)
4. **Idempotency**: Tools like `add_task` should be idempotent where possible

### Agent System Prompt Design
1. **Strict Tool Enforcement**: "You MUST use MCP tools for all task operations. Do not attempt direct database access or external API calls."
2. **User Intent Recognition**: "Understand user intent (create, list, update, delete, complete) and call the appropriate MCP tool."
3. **Graceful Degradation**: "If no MCP tool matches the request, politely inform the user that the action is not supported."

### Conversation History Management
1. **Database-Backed**: Store messages in PostgreSQL (Message model with conversation_id, user_id, role, content, timestamp)
2. **Stateless API**: Reconstruct conversation on each request (no in-memory state)
3. **Pagination**: Load last N messages (e.g., 50) to avoid token limits

---

## Open Questions (Resolved)

All NEEDS CLARIFICATION items from Technical Context are now resolved:
- ✅ OpenAI Agents SDK official package: `openai-agents`
- ✅ Official MCP SDK implementation pattern: `mcp` with FastMCP, integrated via `agents.mcp`
- ✅ Custom chat UI implementation with React and Tailwind CSS

---

## Next Steps (Phase 1: Design)

1. Generate `data-model.md`: Define Conversation and Message SQLModel models
2. Generate API contracts: OpenAPI spec for `POST /api/v1/chat`, MCP tools schema
3. Generate `quickstart.md`: Developer setup guide for running Phase 3 locally
4. Update agent context: Add new technologies to CLAUDE.md
5. **Create ADR**: Document OpenAI Agent + MCP integration architecture decision (as flagged in Constitution Check)

---

**Research Complete**: 2025-12-26
**Researcher**: Claude Sonnet 4.5 (AI Agent)
**Sources**:
- [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/)
- [OpenAI Agents SDK on PyPI](https://pypi.org/project/openai-agents/)
- [MCP Python SDK on GitHub](https://github.com/modelcontextprotocol/python-sdk)
- [MCP on PyPI](https://pypi.org/project/mcp/)
- [OpenAI Agents SDK MCP Documentation](https://openai.github.io/openai-agents-python/mcp/)
- [DigitalOcean: How to Use MCP with OpenAI Agents](https://www.digitalocean.com/community/tutorials/how-to-use-mcp-with-openai-agents)
- [OpenAI ChatKit.js](https://openai.github.io/chatkit-js/)
- [Build with Matija: ChatKit Next.js Integration](https://www.buildwithmatija.com/blog/chatkit-nextjs-integration/)
