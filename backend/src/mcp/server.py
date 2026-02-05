"""
MCP Server for Task Management Tools

This module implements the Model Context Protocol (MCP) server that exposes
task management tools for integration with Claude Desktop.
"""

import asyncio
import logging
from mcp.server.fastmcp import FastMCP
from mcp.server.exceptions import McpError

# Set up logging to stderr to avoid interfering with MCP protocol
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# Initialize the MCP server
mcp = FastMCP(
    name="task-management-mcp",
    version="1.0.0"
)

# Import tool functions
from .tools.task_operations import (
    create_task_mcp,
    list_tasks_mcp,
    complete_task_mcp,
    update_task_mcp,
    delete_task_mcp
)


@mcp.tool()
def add_task(user_id: str, title: str, description: str = None) -> str:
    """
    Add a new task for the specified user.

    Args:
        user_id: The user ID for whom to create the task
        title: The title of the task
        description: Optional description of the task

    Returns:
        JSON string with status and result information
    """
    result = create_task_mcp(user_id, title, description)
    import json
    return json.dumps(result)


@mcp.tool()
def list_tasks(user_id: str, limit: int = 10, offset: int = 0) -> str:
    """
    List tasks for the specified user.

    Args:
        user_id: The user ID whose tasks to list
        limit: Maximum number of tasks to return (default 10)
        offset: Number of tasks to skip (default 0)

    Returns:
        JSON string with status and tasks list
    """
    result = list_tasks_mcp(user_id, limit, offset)
    import json
    return json.dumps(result)


@mcp.tool()
def complete_task(user_id: str, task_id: str) -> str:
    """
    Mark a task as completed for the specified user.

    Args:
        user_id: The user ID
        task_id: The ID of the task to complete

    Returns:
        JSON string with status and result information
    """
    result = complete_task_mcp(user_id, task_id)
    import json
    return json.dumps(result)


@mcp.tool()
def update_task(user_id: str, task_id: str, title: str = None, description: str = None) -> str:
    """
    Update a task for the specified user.

    Args:
        user_id: The user ID
        task_id: The ID of the task to update
        title: New title for the task (optional)
        description: New description for the task (optional)

    Returns:
        JSON string with status and result information
    """
    result = update_task_mcp(user_id, task_id, title, description)
    import json
    return json.dumps(result)


@mcp.tool()
def delete_task(user_id: str, task_id: str) -> str:
    """
    Delete a task for the specified user.

    Args:
        user_id: The user ID
        task_id: The ID of the task to delete

    Returns:
        JSON string with status and result information
    """
    result = delete_task_mcp(user_id, task_id)
    import json
    return json.dumps(result)


def register_tools():
    """
    Register all MCP tools with the server.
    Tools are decorated directly on the mcp object, so this is just for organization.
    """
    logger.info("MCP tools registered successfully")


def main():
    """
    Main entry point for the MCP server.
    Runs the server with stdio transport for Claude Desktop integration.
    """
    logger.info("Starting Task Management MCP Server")

    try:
        # Register all tools
        register_tools()

        # Run the server with stdio transport
        logger.info("MCP server running with stdio transport")
        mcp.run(transport="stdio")

    except KeyboardInterrupt:
        logger.info("MCP server stopped by user")
    except Exception as e:
        logger.error(f"MCP server error: {str(e)}")
        raise


if __name__ == "__main__":
    main()