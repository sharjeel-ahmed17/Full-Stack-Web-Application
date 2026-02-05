"""
Tests for complete_task MCP tool

This module contains tests for the complete_task functionality in the MCP tools.
"""
import pytest
from unittest.mock import patch, MagicMock
from uuid import uuid4, UUID
from datetime import datetime

from src.mcp.tools.task_operations import complete_task_mcp


class TestCompleteTask:
    """Test class for complete_task functionality."""

    def test_complete_task_valid_input(self):
        """Test complete_task with valid input successfully updates task."""
        # Arrange
        user_id = str(uuid4())
        task_id = str(uuid4())

        # Create mock task
        mock_task = MagicMock()
        mock_task.id = uuid4()
        mock_task.title = "Test Task"
        mock_task.is_completed = True

        with patch('src.mcp.tools.task_operations.get_session') as mock_get_session_context:
            mock_session_cm = MagicMock()
            mock_session_cm.__enter__ = MagicMock(return_value=MagicMock())
            mock_session_cm.__exit__ = MagicMock(return_value=None)
            mock_get_session_context.return_value = mock_session_cm

            with patch('src.mcp.tools.task_operations.service_toggle_task_completion', return_value=mock_task) as mock_service:

                # Act
                result = complete_task_mcp(user_id, task_id)

                # Assert
                assert result["status"] == "success"
                assert "completed" in result["message"]
                assert mock_task.title in result["message"]
                mock_service.assert_called_once()

    def test_complete_task_invalid_user_id(self):
        """Test complete_task with invalid user ID returns error."""
        # Arrange
        invalid_user_id = "invalid-uuid"
        task_id = str(uuid4())

        # Act
        result = complete_task_mcp(invalid_user_id, task_id)

        # Assert
        assert result["status"] == "error"
        assert "Invalid user ID format" in result["message"]

    def test_complete_task_invalid_task_id(self):
        """Test complete_task with invalid task ID returns error."""
        # Arrange
        user_id = str(uuid4())
        invalid_task_id = "invalid-uuid"

        # Act
        result = complete_task_mcp(user_id, invalid_task_id)

        # Assert
        assert result["status"] == "error"
        assert "Invalid task ID format" in result["message"]

    def test_complete_task_nonexistent_task(self):
        """Test complete_task with nonexistent task returns error."""
        # Arrange
        user_id = str(uuid4())
        task_id = str(uuid4())

        # Mock the service to return None (task not found)
        with patch('src.mcp.tools.task_operations.get_session') as mock_get_session_context:
            mock_session_cm = MagicMock()
            mock_session_cm.__enter__ = MagicMock(return_value=MagicMock())
            mock_session_cm.__exit__ = MagicMock(return_value=None)
            mock_get_session_context.return_value = mock_session_cm

            with patch('src.mcp.tools.task_operations.service_toggle_task_completion', return_value=None) as mock_service:

                # Act
                result = complete_task_mcp(user_id, task_id)

                # Assert
                assert result["status"] == "error"
                assert "not found or doesn't belong to user" in result["message"]
                mock_service.assert_called_once()

    def test_complete_already_completed_task(self):
        """Test complete_task with already completed task (toggles to incomplete)."""
        # Arrange
        user_id = str(uuid4())
        task_id = str(uuid4())

        # Create mock task that is currently completed
        mock_task = MagicMock()
        mock_task.id = uuid4()
        mock_task.title = "Test Task"
        mock_task.is_completed = False  # After toggling, it becomes incomplete

        with patch('src.mcp.tools.task_operations.get_session') as mock_get_session_context:
            mock_session_cm = MagicMock()
            mock_session_cm.__enter__ = MagicMock(return_value=MagicMock())
            mock_session_cm.__exit__ = MagicMock(return_value=None)
            mock_get_session_context.return_value = mock_session_cm

            with patch('src.mcp.tools.task_operations.service_toggle_task_completion', return_value=mock_task) as mock_service:

                # Act
                result = complete_task_mcp(user_id, task_id)

                # Assert
                assert result["status"] == "success"
                assert "marked as incomplete" in result["message"] or "completed" in result["message"]
                mock_service.assert_called_once()

    def test_complete_task_database_error(self):
        """Test complete_task handles database errors gracefully."""
        # Arrange
        user_id = str(uuid4())
        task_id = str(uuid4())

        with patch('src.mcp.tools.task_operations.get_session') as mock_get_session_context:
            mock_session_cm = MagicMock()
            mock_session_cm.__enter__ = MagicMock(side_effect=Exception("DB Connection failed"))
            mock_session_cm.__exit__ = MagicMock(return_value=None)
            mock_get_session_context.return_value = mock_session_cm

            # Act
            result = complete_task_mcp(user_id, task_id)

            # Assert
            assert result["status"] == "error"
            assert "Failed to complete task" in result["message"]

    def test_complete_task_validation_error_handling(self):
        """Test that validation errors are properly handled."""
        # Arrange
        invalid_user_id = "invalid-uuid"
        invalid_task_id = "also-invalid-uuid"

        # Act & Assert
        result = complete_task_mcp(invalid_user_id, invalid_task_id)
        assert result["status"] == "error"
        assert "Invalid user ID format" in result["message"]