# Quickstart: MCP Server & Tools

## Overview
This guide explains how to set up and run the MCP server for task management tools.

## Prerequisites
- Python 3.13+
- uv package manager
- PostgreSQL database (Neon recommended)
- Claude Desktop or MCP-compatible client

## Setup

### 1. Install Dependencies
```bash
# Navigate to the backend directory
cd backend

# Install dependencies using uv
uv pip install -r requirements.txt
```

### 2. Environment Configuration
Create a `.env` file in the backend directory:
```env
DATABASE_URL=postgresql+asyncpg://username:password@localhost/dbname
NEON_DATABASE_URL=postgresql+asyncpg://...
UV_INSTALL_VERBOSE=true
```

### 3. Database Setup
Run database migrations:
```bash
# From backend directory
alembic upgrade head
```

## Running the MCP Server

### 1. Start the MCP Server
```bash
# From backend directory
python -m src.mcp.server
```

Or use the startup script:
```bash
# From backend directory
python start_mcp_server.py
```

### 2. Using the Tools
Once started, the MCP server exposes these tools:
- `add_task`: Create new tasks
- `list_tasks`: Retrieve user's tasks
- `complete_task`: Mark tasks as completed
- `update_task`: Modify task details
- `delete_task`: Remove tasks

### 3. Tool Examples
```bash
# Add a new task
add_task(user_id="uuid-string", title="Sample Task", description="Description here")

# List tasks for a user
list_tasks(user_id="uuid-string")

# Complete a task
complete_task(user_id="uuid-string", task_id="task-uuid")

# Update a task
update_task(user_id="uuid-string", task_id="task-uuid", title="Updated Title")

# Delete a task
delete_task(user_id="uuid-string", task_id="task-uuid")
```

## Development

### Adding New Tools
To add a new MCP tool:
1. Define the tool function with proper type hints
2. Add the @mcp.tool() decorator
3. Implement using existing service layer functions
4. Ensure statelessness and user isolation

### Testing Tools
Run the MCP server tests:
```bash
# Run all MCP tests
pytest tests/mcp/

# Run specific tool tests
pytest tests/mcp/test_add_task.py
pytest tests/mcp/test_list_tasks.py
pytest tests/mcp/test_complete_task.py
pytest tests/mcp/test_update_task.py
pytest tests/mcp/test_delete_task.py
```

## Troubleshooting

### Common Issues
- **Connection errors**: Verify DATABASE_URL is properly set
- **Authentication errors**: Ensure user_id is valid and authenticated
- **Permission errors**: Check that user owns the requested resource
- **Format errors**: Verify UUID strings are in correct format

### Logging
Logs are written to stderr for debugging without interfering with MCP protocol.

## Architecture
- **Statelessness**: Each tool call operates independently with no shared state
- **Database Integration**: Uses the same SQLModel services as the main backend
- **Security**: Enforces user isolation via user_id validation
- **Error Handling**: Comprehensive validation and error reporting