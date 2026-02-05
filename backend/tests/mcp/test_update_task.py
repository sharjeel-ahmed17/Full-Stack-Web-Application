"""
Tests for update_task MCP tool

This module contains tests for the update_task functionality in the MCP tools.
"""
import pytest
from unittest.mock import patch, MagicMock
from uuid import uuid4, UUID
from datetime import datetime

from src.mcp.tools.task_operations import update_task_mcp


class TestUpdateTask:
    """Test class for update_task functionality."""

    def test_update_task_valid_input(self):
        """Test update_task with valid input successfully updates task."""
        # Arrange
        user_id = str(uuid4())
        task_id = str(uuid4())
        new_title = "Updated Task Title"
        new_description = "Updated Description"

        # Create mock updated task
        mock_task = MagicMock()
        mock_task.id = uuid4()
        mock_task.title = new_title
        mock_task.description = new_description
        mock_task.is_completed = False

        with patch('src.mcp.tools.task_operations.get_session') as mock_get_session_context:
            mock_session_cm = MagicMock()
            mock_session_cm.__enter__ = MagicMock(return_value=MagicMock())
            mock_session_cm.__exit__ = MagicMock(return_value=None)
            mock_get_session_context.return_value = mock_session_cm

            with patch('src.mcp.tools.task_operations.service_update_task', return_value=mock_task) as mock_service:

                # Act
                result = update_task_mcp(user_id, task_id, new_title, new_description)

                # Assert
                assert result["status"] == "success"
                assert "updated successfully" in result["message"]
                assert new_title in result["message"]
                mock_service.assert_called_once()

    def test_update_task_invalid_user_id(self):
        """Test update_task with invalid user ID returns error."""
        # Arrange
        invalid_user_id = "invalid-uuid"
        task_id = str(uuid4())
        new_title = "Updated Task Title"

        # Act
        result = update_task_mcp(invalid_user_id, task_id, new_title)

        # Assert
        assert result["status"] == "error"
        assert "Invalid user ID format" in result["message"]

    def test_update_task_invalid_task_id(self):
        """Test update_task with invalid task ID returns error."""
        # Arrange
        user_id = str(uuid4())
        invalid_task_id = "invalid-uuid"
        new_title = "Updated Task Title"

        # Act
        result = update_task_mcp(user_id, invalid_task_id, new_title)

        # Assert
        assert result["status"] == "error"
        assert "Invalid task ID format" in result["message"]

    def test_update_task_nonexistent_task(self):
        """Test update_task with nonexistent task returns error."""
        # Arrange
        user_id = str(uuid4())
        task_id = str(uuid4())
        new_title = "Updated Task Title"

        # Mock the service to return None (task not found)
        with patch('src.mcp.tools.task_operations.get_session') as mock_get_session_context:
            mock_session_cm = MagicMock()
            mock_session_cm.__enter__ = MagicMock(return_value=MagicMock())
            mock_session_cm.__exit__ = MagicMock(return_value=None)
            mock_get_session_context.return_value = mock_session_cm

            with patch('src.mcp.tools.task_operations.service_update_task', return_value=None) as mock_service:

                # Act
                result = update_task_mcp(user_id, task_id, new_title)

                # Assert
                assert result["status"] == "error"
                assert "not found or doesn't belong to user" in result["message"]
                mock_service.assert_called_once()

    def test_update_task_partial_update_title_only(self):
        """Test update_task with partial update (title only)."""
        # Arrange
        user_id = str(uuid4())
        task_id = str(uuid4())
        new_title = "Updated Task Title"

        # Create mock updated task
        mock_task = MagicMock()
        mock_task.id = uuid4()
        mock_task.title = new_title
        mock_task.description = "Original Description"
        mock_task.is_completed = False

        with patch('src.mcp.tools.task_operations.get_session') as mock_get_session_context:
            mock_session_cm = MagicMock()
            mock_session_cm.__enter__ = MagicMock(return_value=MagicMock())
            mock_session_cm.__exit__ = MagicMock(return_value=None)
            mock_get_session_context.return_value = mock_session_cm

            with patch('src.mcp.tools.task_operations.service_update_task', return_value=mock_task) as mock_service:

                # Act
                result = update_task_mcp(user_id, task_id, title=new_title)

                # Assert
                assert result["status"] == "success"
                assert "updated successfully" in result["message"]
                assert new_title in result["message"]
                mock_service.assert_called_once()

    def test_update_task_partial_update_description_only(self):
        """Test update_task with partial update (description only)."""
        # Arrange
        user_id = str(uuid4())
        task_id = str(uuid4())
        new_description = "Updated Description"

        # Create mock updated task
        mock_task = MagicMock()
        mock_task.id = uuid4()
        mock_task.title = "Original Title"
        mock_task.description = new_description
        mock_task.is_completed = False

        with patch('src.mcp.tools.task_operations.get_session') as mock_get_session_context:
            mock_session_cm = MagicMock()
            mock_session_cm.__enter__ = MagicMock(return_value=MagicMock())
            mock_session_cm.__exit__ = MagicMock(return_value=None)
            mock_get_session_context.return_value = mock_session_cm

            with patch('src.mcp.tools.task_operations.service_update_task', return_value=mock_task) as mock_service:

                # Act
                result = update_task_mcp(user_id, task_id, description=new_description)

                # Assert
                assert result["status"] == "success"
                assert "updated successfully" in result["message"]
                mock_service.assert_called_once()

    def test_update_task_database_error(self):
        """Test update_task handles database errors gracefully."""
        # Arrange
        user_id = str(uuid4())
        task_id = str(uuid4())
        new_title = "Updated Task Title"

        with patch('src.mcp.tools.task_operations.get_session') as mock_get_session_context:
            mock_session_cm = MagicMock()
            mock_session_cm.__enter__ = MagicMock(side_effect=Exception("DB Connection failed"))
            mock_session_cm.__exit__ = MagicMock(return_value=None)
            mock_get_session_context.return_value = mock_session_cm

            # Act
            result = update_task_mcp(user_id, task_id, new_title)

            # Assert
            assert result["status"] == "error"
            assert "Failed to update task" in result["message"]

    def test_update_task_long_title_error(self):
        """Test update_task with too long title returns error."""
        # Arrange
        user_id = str(uuid4())
        task_id = str(uuid4())
        long_title = "A" * 201  # Too long

        # Act
        result = update_task_mcp(user_id, task_id, title=long_title)

        # Assert
        assert result["status"] == "error"
        assert "Task title must be 200 characters or less" in result["message"]

    def test_update_task_validation_error_handling(self):
        """Test that validation errors are properly handled."""
        # Arrange
        invalid_user_id = "invalid-uuid"
        invalid_task_id = "also-invalid-uuid"

        # Act & Assert
        result = update_task_mcp(invalid_user_id, invalid_task_id, title="Valid title")
        assert result["status"] == "error"
        assert "Invalid user ID format" in result["message"]