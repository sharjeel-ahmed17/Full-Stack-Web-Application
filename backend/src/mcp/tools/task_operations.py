"""
MCP Task Operations Implementation

This module implements the core task management operations for MCP tools,
integrating with the existing SQLModel services while ensuring proper
validation and error handling.
"""

import logging
from typing import Dict, Any, Optional
from uuid import UUID

from ...database import get_session
from ...services.tasks import (
    create_task as service_create_task,
    list_user_tasks as service_list_user_tasks,
    toggle_task_completion as service_toggle_task_completion,
    update_task as service_update_task,
    delete_task as service_delete_task,
    get_user_task as service_get_user_task
)
from ...models.task import TaskCreate
from .validators import (
    TaskValidator,
    AddTaskInput,
    ListTasksInput,
    CompleteTaskInput,
    UpdateTaskInput,
    DeleteTaskInput
)

# Set up logging
logger = logging.getLogger(__name__)


def create_task_mcp(user_id_str: str, title: str, description: Optional[str] = None) -> Dict[str, Any]:
    """
    MCP wrapper for creating a new task.

    Args:
        user_id_str: String representation of user UUID
        title: Task title
        description: Optional task description

    Returns:
        Dictionary with operation result
    """
    try:
        # Validate inputs
        user_id = TaskValidator.validate_user_id(user_id_str)
        validated_title = TaskValidator.validate_task_title(title)
        validated_description = TaskValidator.validate_task_description(description)

        # Create the input model for validation
        validated_input = AddTaskInput(
            user_id=str(user_id),
            title=validated_title,
            description=validated_description
        )

        # Create the TaskCreate model (without user_id since it's passed separately to the service)
        task_create = TaskCreate(
            title=validated_input.title,
            description=validated_input.description
        )

        # Use database session
        with get_session() as session:
            new_task = service_create_task(session, task_create, user_id)

            return {
                "status": "success",
                "task_id": str(new_task.id),
                "message": f"Task '{new_task.title}' created successfully"
            }

    except ValueError as e:
        logger.error(f"Validation error in create_task: {str(e)}")
        return {
            "status": "error",
            "message": str(e)
        }
    except Exception as e:
        logger.error(f"Unexpected error in create_task: {str(e)}")
        return {
            "status": "error",
            "message": "Failed to create task"
        }


def list_tasks_mcp(user_id_str: str, limit: Optional[int] = None, offset: Optional[int] = None) -> Dict[str, Any]:
    """
    MCP wrapper for listing user tasks.

    Args:
        user_id_str: String representation of user UUID
        limit: Maximum number of tasks to return
        offset: Number of tasks to skip

    Returns:
        Dictionary with operation result and tasks list
    """
    try:
        # Validate inputs
        user_id = TaskValidator.validate_user_id(user_id_str)
        validated_limit, validated_offset = TaskValidator.validate_pagination_params(limit, offset)

        # Create the input model for validation
        validated_input = ListTasksInput(
            user_id=str(user_id),
            limit=validated_limit,
            offset=validated_offset
        )

        # Use database session
        with get_session() as session:
            tasks = service_list_user_tasks(
                session,
                user_id,
                skip=validated_input.offset,
                limit=validated_input.limit
            )

            tasks_data = []
            for task in tasks:
                task_dict = {
                    "id": str(task.id),
                    "title": task.title,
                    "description": task.description or "",
                    "is_completed": task.is_completed,
                    "created_at": task.created_at.isoformat() if task.created_at else None,
                    "updated_at": task.updated_at.isoformat() if task.updated_at else None
                }
                tasks_data.append(task_dict)

            return {
                "status": "success",
                "tasks": tasks_data,
                "total_count": len(tasks_data),
                "message": f"Retrieved {len(tasks_data)} tasks for user"
            }

    except ValueError as e:
        logger.error(f"Validation error in list_tasks: {str(e)}")
        return {
            "status": "error",
            "message": str(e)
        }
    except Exception as e:
        logger.error(f"Unexpected error in list_tasks: {str(e)}")
        return {
            "status": "error",
            "message": "Failed to retrieve tasks"
        }


def complete_task_mcp(user_id_str: str, task_id_str: str) -> Dict[str, Any]:
    """
    MCP wrapper for completing a task.

    Args:
        user_id_str: String representation of user UUID
        task_id_str: String representation of task UUID

    Returns:
        Dictionary with operation result
    """
    try:
        # Validate inputs
        user_id = TaskValidator.validate_user_id(user_id_str)
        task_id = TaskValidator.validate_task_id(task_id_str)

        # Create the input model for validation
        validated_input = CompleteTaskInput(
            user_id=str(user_id),
            task_id=str(task_id)
        )

        # Use database session
        with get_session() as session:
            updated_task = service_toggle_task_completion(session, task_id, user_id)

            if updated_task is None:
                return {
                    "status": "error",
                    "message": f"Task with ID {task_id_str} not found or doesn't belong to user"
                }

            status_msg = "completed" if updated_task.is_completed else "marked as incomplete"
            return {
                "status": "success",
                "message": f"Task '{updated_task.title}' {status_msg}"
            }

    except ValueError as e:
        logger.error(f"Validation error in complete_task: {str(e)}")
        return {
            "status": "error",
            "message": str(e)
        }
    except Exception as e:
        logger.error(f"Unexpected error in complete_task: {str(e)}")
        return {
            "status": "error",
            "message": "Failed to complete task"
        }


def update_task_mcp(
    user_id_str: str,
    task_id_str: str,
    title: Optional[str] = None,
    description: Optional[str] = None
) -> Dict[str, Any]:
    """
    MCP wrapper for updating a task.

    Args:
        user_id_str: String representation of user UUID
        task_id_str: String representation of task UUID
        title: New task title (optional)
        description: New task description (optional)

    Returns:
        Dictionary with operation result
    """
    try:
        # Validate inputs
        user_id = TaskValidator.validate_user_id(user_id_str)
        task_id = TaskValidator.validate_task_id(task_id_str)

        if title is not None:
            title = TaskValidator.validate_task_title(title)
        if description is not None:
            description = TaskValidator.validate_task_description(description)

        # Create the input model for validation
        validated_input = UpdateTaskInput(
            user_id=str(user_id),
            task_id=str(task_id),
            title=title,
            description=description
        )

        # Use database session
        with get_session() as session:
            updated_task = service_update_task(
                session,
                task_id,
                user_id,
                title=validated_input.title,
                description=validated_input.description
            )

            if updated_task is None:
                return {
                    "status": "error",
                    "message": f"Task with ID {task_id_str} not found or doesn't belong to user"
                }

            return {
                "status": "success",
                "message": f"Task '{updated_task.title}' updated successfully"
            }

    except ValueError as e:
        logger.error(f"Validation error in update_task: {str(e)}")
        return {
            "status": "error",
            "message": str(e)
        }
    except Exception as e:
        logger.error(f"Unexpected error in update_task: {str(e)}")
        return {
            "status": "error",
            "message": "Failed to update task"
        }


def delete_task_mcp(user_id_str: str, task_id_str: str) -> Dict[str, Any]:
    """
    MCP wrapper for deleting a task.

    Args:
        user_id_str: String representation of user UUID
        task_id_str: String representation of task UUID

    Returns:
        Dictionary with operation result
    """
    try:
        # Validate inputs
        user_id = TaskValidator.validate_user_id(user_id_str)
        task_id = TaskValidator.validate_task_id(task_id_str)

        # Create the input model for validation
        validated_input = DeleteTaskInput(
            user_id=str(user_id),
            task_id=str(task_id)
        )

        # Use database session
        with get_session() as session:
            success = service_delete_task(session, task_id, user_id)

            if not success:
                return {
                    "status": "error",
                    "message": f"Task with ID {task_id_str} not found or doesn't belong to user"
                }

            return {
                "status": "success",
                "message": "Task deleted successfully"
            }

    except ValueError as e:
        logger.error(f"Validation error in delete_task: {str(e)}")
        return {
            "status": "error",
            "message": str(e)
        }
    except Exception as e:
        logger.error(f"Unexpected error in delete_task: {str(e)}")
        return {
            "status": "error",
            "message": "Failed to delete task"
        }