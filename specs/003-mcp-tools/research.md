# MCP Server & Tools Research

## Decision: MCP SDK Implementation with FastAPI and SQLModel Integration
**Rationale**: The implementation will leverage the Official MCP SDK (mcp v1.25.0+) with FastAPI backend integration and SQLModel database operations, reusing existing service patterns from the current codebase.

## Alternatives Considered
- **Separate MCP Server Process**: Standalone server that shares database layer with FastAPI backend
- **Integrated MCP in FastAPI App**: Adding MCP endpoints directly to existing FastAPI application
- **Custom MCP Implementation**: Building MCP protocol from scratch instead of using FastMCP

## Key Findings

### 1. MCP SDK and FastMCP
- **Decision**: Use FastMCP from the Official MCP SDK (v1.25.0+) for simplified implementation
- **Rationale**: FastMCP provides the most reliable and simplest MCP implementation, following established patterns
- **Implementation Pattern**:
  ```python
  from mcp.server.fastmcp import FastMCP
  mcp = FastMCP("task-mcp")

  @mcp.tool()
  async def add_task(user_id: str, title: str, description: str = None) -> str:
      """Create a new task for a user."""
      # Implementation using existing SQLModel services
  ```

### 2. Database Integration
- **Decision**: Reuse existing SQLModel service layer from `backend/src/services/tasks.py`
- **Rationale**: Leverages proven, secure, and well-tested database operations with proper user isolation
- **Pattern**: MCP tools will call the same service functions as FastAPI endpoints

### 3. Transport Method
- **Decision**: Use stdio transport for Claude Desktop integration
- **Rationale**: Standard transport mechanism for MCP servers in desktop environments

### 4. Architecture Pattern
- **Decision**: Separate MCP Server Process with shared database layer
- **Rationale**: Maintains clear separation of concerns while enabling code reuse

## Required Tools Implementation
Based on spec requirements, 5 MCP tools need implementation:
1. `add_task`: Create new tasks using existing `create_task` service
2. `list_tasks`: Retrieve tasks using existing `list_user_tasks` service
3. `complete_task`: Update completion status using existing update service
4. `update_task`: Modify task details using existing `update_task` service
5. `delete_task`: Remove tasks using existing `delete_task` service

## Implementation Constraints
- **Statelessness**: Tools must hold no memory between calls
- **User Isolation**: All operations must enforce `user_id` filtering
- **Input Validation**: Strict validation following existing patterns
- **Error Handling**: Structured, user-friendly error messages
- **Logging**: Use stderr to avoid protocol corruption