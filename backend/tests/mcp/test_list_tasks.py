"""
Tests for list_tasks MCP tool

This module contains tests for the list_tasks functionality in the MCP tools.
"""
import pytest
from unittest.mock import patch, MagicMock
from uuid import uuid4, UUID
from datetime import datetime

from src.mcp.tools.task_operations import list_tasks_mcp


class TestListTasks:
    """Test class for list_tasks functionality."""

    def test_list_tasks_valid_user_with_tasks(self):
        """Test list_tasks with valid user ID returns their tasks."""
        # Arrange
        user_id = str(uuid4())

        # Create mock tasks
        mock_task1 = MagicMock()
        mock_task1.id = uuid4()
        mock_task1.title = "Task 1"
        mock_task1.description = "Description 1"
        mock_task1.is_completed = False
        mock_task1.created_at = datetime.now()
        mock_task1.updated_at = datetime.now()

        mock_task2 = MagicMock()
        mock_task2.id = uuid4()
        mock_task2.title = "Task 2"
        mock_task2.description = "Description 2"
        mock_task2.is_completed = True
        mock_task2.created_at = datetime.now()
        mock_task2.updated_at = datetime.now()

        mock_tasks = [mock_task1, mock_task2]

        with patch('src.mcp.tools.task_operations.get_session') as mock_get_session_context:
            mock_session_cm = MagicMock()
            mock_session_cm.__enter__ = MagicMock(return_value=MagicMock())
            mock_session_cm.__exit__ = MagicMock(return_value=None)
            mock_get_session_context.return_value = mock_session_cm

            with patch('src.mcp.tools.task_operations.service_list_user_tasks', return_value=mock_tasks) as mock_service:

                # Act
                result = list_tasks_mcp(user_id)

                # Assert
                assert result["status"] == "success"
                assert result["total_count"] == 2
                assert len(result["tasks"]) == 2
                assert result["message"] == "Retrieved 2 tasks for user"
                mock_service.assert_called_once()

    def test_list_tasks_valid_user_no_tasks(self):
        """Test list_tasks with valid user ID but no tasks returns empty list."""
        # Arrange
        user_id = str(uuid4())
        mock_tasks = []

        with patch('src.mcp.tools.task_operations.get_session') as mock_get_session_context:
            mock_session_cm = MagicMock()
            mock_session_cm.__enter__ = MagicMock(return_value=MagicMock())
            mock_session_cm.__exit__ = MagicMock(return_value=None)
            mock_get_session_context.return_value = mock_session_cm

            with patch('src.mcp.tools.task_operations.service_list_user_tasks', return_value=mock_tasks) as mock_service:

                # Act
                result = list_tasks_mcp(user_id)

                # Assert
                assert result["status"] == "success"
                assert result["total_count"] == 0
                assert len(result["tasks"]) == 0
                assert result["message"] == "Retrieved 0 tasks for user"
                mock_service.assert_called_once()

    def test_list_tasks_invalid_user_id(self):
        """Test list_tasks with invalid user ID returns error."""
        # Arrange
        invalid_user_id = "invalid-uuid"

        # Act
        result = list_tasks_mcp(invalid_user_id)

        # Assert
        assert result["status"] == "error"
        assert "Invalid user ID format" in result["message"]

    def test_list_tasks_with_pagination(self):
        """Test list_tasks with pagination parameters."""
        # Arrange
        user_id = str(uuid4())
        limit = 5
        offset = 2
        mock_tasks = []  # Empty list for this test

        with patch('src.mcp.tools.task_operations.get_session') as mock_get_session_context:
            mock_session_cm = MagicMock()
            mock_session_cm.__enter__ = MagicMock(return_value=MagicMock())
            mock_session_cm.__exit__ = MagicMock(return_value=None)
            mock_get_session_context.return_value = mock_session_cm

            with patch('src.mcp.tools.task_operations.service_list_user_tasks', return_value=mock_tasks) as mock_service:

                # Act
                result = list_tasks_mcp(user_id, limit, offset)

                # Assert
                assert result["status"] == "success"
                assert result["total_count"] == 0
                assert len(result["tasks"]) == 0
                mock_service.assert_called_once_with(MagicMock(), UUID(user_id), skip=offset, limit=limit)

    def test_list_tasks_with_invalid_pagination(self):
        """Test list_tasks with invalid pagination parameters returns error."""
        # Arrange
        user_id = str(uuid4())
        invalid_limit = 0  # Less than 1

        # Act
        result = list_tasks_mcp(user_id, invalid_limit)

        # Assert
        assert result["status"] == "error"
        assert "limit must be between 1 and 100" in result["message"]

    def test_list_tasks_database_error(self):
        """Test list_tasks handles database errors gracefully."""
        # Arrange
        user_id = str(uuid4())

        with patch('src.mcp.tools.task_operations.get_session') as mock_get_session_context:
            mock_session_cm = MagicMock()
            mock_session_cm.__enter__ = MagicMock(side_effect=Exception("DB Connection failed"))
            mock_session_cm.__exit__ = MagicMock(return_value=None)
            mock_get_session_context.return_value = mock_session_cm

            # Act
            result = list_tasks_mcp(user_id)

            # Assert
            assert result["status"] == "error"
            assert "Failed to retrieve tasks" in result["message"]

    def test_list_tasks_validation_error_handling(self):
        """Test that validation errors are properly handled."""
        # Arrange
        user_id = "invalid-uuid"  # Invalid user ID format

        # Act & Assert
        result = list_tasks_mcp(user_id)
        assert result["status"] == "error"
        assert "Invalid user ID format" in result["message"]