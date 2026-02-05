from typing import Dict, Any, List
from uuid import UUID
import requests
from ..core.config import settings


class MCPTaskTools:
    """
    MCP tools for task management operations (add/list/complete/update/delete).

    These tools are callable by AI agents to perform task management operations.
    """

    def __init__(self):
        self.mcp_server_url = settings.mcp_server_url

    def _make_mcp_request(self, method: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Wrapper for making requests to the MCP server with error handling.

        Args:
            method: The MCP method to call
            params: Parameters for the method

        Returns:
            Dict containing the result of the operation
        """
        try:
            # Construct the payload for the MCP server
            payload = {
                "method": method,
                "params": params
            }

            # Call the MCP server
            response = requests.post(
                f"{self.mcp_server_url}/invoke",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=10  # Add timeout to prevent hanging requests
            )

            if response.status_code == 200:
                try:
                    result = response.json()
                    return {
                        "success": True,
                        "result": result
                    }
                except ValueError:
                    # Response is not JSON
                    return {
                        "success": True,
                        "result": response.text
                    }
            else:
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}: {response.text}",
                    "status_code": response.status_code
                }
        except requests.exceptions.Timeout:
            return {
                "success": False,
                "error": "Request timed out while connecting to MCP server"
            }
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "error": "Connection error: Unable to reach MCP server"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Unexpected error occurred while communicating with MCP server: {str(e)}"
            }

    def add_task(self, user_id: str, title: str, description: str = "") -> Dict[str, Any]:
        """
        Add a new task using MCP tools.

        Args:
            user_id: ID of the user who owns the task
            title: Title of the task
            description: Optional description of the task

        Returns:
            Dict containing the result of the operation
        """
        try:
            # Validate inputs
            if not title or title.strip() == "":
                return {
                    "success": False,
                    "error": "Task title cannot be empty"
                }

            # Make the MCP request
            result = self._make_mcp_request(
                method="tasks/add",
                params={
                    "user_id": user_id,
                    "title": title,
                    "description": description
                }
            )

            if result["success"]:
                task_result = result["result"]
                return {
                    "success": True,
                    "message": f"Task '{title}' created successfully",
                    "task_id": task_result.get("task_id", "unknown") if isinstance(task_result, dict) else "unknown"
                }
            else:
                return {
                    "success": False,
                    "error": result["error"]
                }

        except Exception as e:
            return {
                "success": False,
                "error": f"Exception occurred while creating task: {str(e)}"
            }

    def list_tasks(self, user_id: str, status: str = "all") -> Dict[str, Any]:
        """
        List tasks for a user using MCP tools.

        Args:
            user_id: ID of the user whose tasks to list
            status: Filter by status ('all', 'pending', 'completed')

        Returns:
            Dict containing the list of tasks
        """
        try:
            # Make the MCP request
            result = self._make_mcp_request(
                method="tasks/list",
                params={
                    "user_id": user_id,
                    "status": status
                }
            )

            if result["success"]:
                task_result = result["result"]

                # Handle both dict and other types of results
                if isinstance(task_result, dict):
                    tasks = task_result.get("tasks", [])

                    if status != "all":
                        if status == "pending":
                            tasks = [task for task in tasks if not task.get("is_completed", False)]
                        elif status == "completed":
                            tasks = [task for task in tasks if task.get("is_completed", False)]

                    return {
                        "success": True,
                        "tasks": tasks,
                        "count": len(tasks)
                    }
                else:
                    return {
                        "success": True,
                        "tasks": [],
                        "count": 0
                    }
            else:
                return {
                    "success": False,
                    "error": result["error"]
                }

        except Exception as e:
            return {
                "success": False,
                "error": f"Exception occurred while listing tasks: {str(e)}"
            }

    def update_task(self, user_id: str, task_id: str, title: str = None, description: str = None, is_completed: bool = None) -> Dict[str, Any]:
        """
        Update a task using MCP tools.

        Args:
            user_id: ID of the user who owns the task
            task_id: ID of the task to update
            title: New title for the task (optional)
            description: New description for the task (optional)
            is_completed: New completion status (optional)

        Returns:
            Dict containing the result of the operation
        """
        try:
            # Validate inputs
            if not task_id or task_id.strip() == "":
                return {
                    "success": False,
                    "error": "Task ID cannot be empty"
                }

            # Construct the parameters
            params = {
                "user_id": user_id,
                "task_id": task_id
            }

            if title is not None:
                params["title"] = title
            if description is not None:
                params["description"] = description
            if is_completed is not None:
                params["is_completed"] = is_completed

            # Make the MCP request
            result = self._make_mcp_request(
                method="tasks/update",
                params=params
            )

            if result["success"]:
                return {
                    "success": True,
                    "message": f"Task '{task_id}' updated successfully"
                }
            else:
                return {
                    "success": False,
                    "error": result["error"]
                }

        except Exception as e:
            return {
                "success": False,
                "error": f"Exception occurred while updating task: {str(e)}"
            }

    def delete_task(self, user_id: str, task_id: str) -> Dict[str, Any]:
        """
        Delete a task using MCP tools.

        Args:
            user_id: ID of the user who owns the task
            task_id: ID of the task to delete

        Returns:
            Dict containing the result of the operation
        """
        try:
            # Validate inputs
            if not task_id or task_id.strip() == "":
                return {
                    "success": False,
                    "error": "Task ID cannot be empty"
                }

            # Make the MCP request
            result = self._make_mcp_request(
                method="tasks/delete",
                params={
                    "user_id": user_id,
                    "task_id": task_id
                }
            )

            if result["success"]:
                return {
                    "success": True,
                    "message": f"Task '{task_id}' deleted successfully"
                }
            else:
                return {
                    "success": False,
                    "error": result["error"]
                }

        except Exception as e:
            return {
                "success": False,
                "error": f"Exception occurred while deleting task: {str(e)}"
            }

    def complete_task(self, user_id: str, task_id: str) -> Dict[str, Any]:
        """
        Mark a task as complete using MCP tools.

        Args:
            user_id: ID of the user who owns the task
            task_id: ID of the task to complete

        Returns:
            Dict containing the result of the operation
        """
        try:
            # Validate inputs
            if not task_id or task_id.strip() == "":
                return {
                    "success": False,
                    "error": "Task ID cannot be empty"
                }

            # Make the MCP request
            result = self._make_mcp_request(
                method="tasks/complete",
                params={
                    "user_id": user_id,
                    "task_id": task_id
                }
            )

            if result["success"]:
                return {
                    "success": True,
                    "message": f"Task '{task_id}' marked as complete"
                }
            else:
                return {
                    "success": False,
                    "error": result["error"]
                }

        except Exception as e:
            return {
                "success": False,
                "error": f"Exception occurred while completing task: {str(e)}"
            }


# Initialize the MCP tools instance
mcp_task_tools = MCPTaskTools()