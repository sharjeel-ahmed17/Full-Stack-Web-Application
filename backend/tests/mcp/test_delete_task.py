"""
Tests for delete_task MCP tool

This module contains tests for the delete_task functionality in the MCP tools.
"""
import pytest
from unittest.mock import patch, MagicMock
from uuid import uuid4, UUID

from src.mcp.tools.task_operations import delete_task_mcp


class TestDeleteTask:
    """Test class for delete_task functionality."""

    def test_delete_task_valid_input(self):
        """Test delete_task with valid input successfully deletes task."""
        # Arrange
        user_id = str(uuid4())
        task_id = str(uuid4())

        # Mock the service to return True for successful deletion
        with patch('src.mcp.tools.task_operations.get_session') as mock_get_session_context:
            mock_session_cm = MagicMock()
            mock_session_cm.__enter__ = MagicMock(return_value=MagicMock())
            mock_session_cm.__exit__ = MagicMock(return_value=None)
            mock_get_session_context.return_value = mock_session_cm

            with patch('src.mcp.tools.task_operations.service_delete_task', return_value=True) as mock_service:

                # Act
                result = delete_task_mcp(user_id, task_id)

                # Assert
                assert result["status"] == "success"
                assert "deleted successfully" in result["message"]
                mock_service.assert_called_once()

    def test_delete_task_invalid_user_id(self):
        """Test delete_task with invalid user ID returns error."""
        # Arrange
        invalid_user_id = "invalid-uuid"
        task_id = str(uuid4())

        # Act
        result = delete_task_mcp(invalid_user_id, task_id)

        # Assert
        assert result["status"] == "error"
        assert "Invalid user ID format" in result["message"]

    def test_delete_task_invalid_task_id(self):
        """Test delete_task with invalid task ID returns error."""
        # Arrange
        user_id = str(uuid4())
        invalid_task_id = "invalid-uuid"

        # Act
        result = delete_task_mcp(user_id, invalid_task_id)

        # Assert
        assert result["status"] == "error"
        assert "Invalid task ID format" in result["message"]

    def test_delete_task_nonexistent_task(self):
        """Test delete_task with nonexistent task returns error."""
        # Arrange
        user_id = str(uuid4())
        task_id = str(uuid4())

        # Mock the service to return False for unsuccessful deletion
        with patch('src.mcp.tools.task_operations.get_session') as mock_get_session_context:
            mock_session_cm = MagicMock()
            mock_session_cm.__enter__ = MagicMock(return_value=MagicMock())
            mock_session_cm.__exit__ = MagicMock(return_value=None)
            mock_get_session_context.return_value = mock_session_cm

            with patch('src.mcp.tools.task_operations.service_delete_task', return_value=False) as mock_service:

                # Act
                result = delete_task_mcp(user_id, task_id)

                # Assert
                assert result["status"] == "error"
                assert "not found or doesn't belong to user" in result["message"]
                mock_service.assert_called_once()

    def test_delete_task_from_different_user(self):
        """Test delete_task with task that belongs to different user returns error."""
        # This is handled by the underlying service which checks user ownership
        # Arrange
        user_id = str(uuid4())
        task_id = str(uuid4())

        # Mock the service to return False to simulate task not owned by user
        with patch('src.mcp.tools.task_operations.get_session') as mock_get_session_context:
            mock_session_cm = MagicMock()
            mock_session_cm.__enter__ = MagicMock(return_value=MagicMock())
            mock_session_cm.__exit__ = MagicMock(return_value=None)
            mock_get_session_context.return_value = mock_session_cm

            with patch('src.mcp.tools.task_operations.service_delete_task', return_value=False) as mock_service:

                # Act
                result = delete_task_mcp(user_id, task_id)

                # Assert
                assert result["status"] == "error"
                assert "not found or doesn't belong to user" in result["message"]
                mock_service.assert_called_once()

    def test_delete_task_database_error(self):
        """Test delete_task handles database errors gracefully."""
        # Arrange
        user_id = str(uuid4())
        task_id = str(uuid4())

        with patch('src.mcp.tools.task_operations.get_session') as mock_get_session_context:
            mock_session_cm = MagicMock()
            mock_session_cm.__enter__ = MagicMock(side_effect=Exception("DB Connection failed"))
            mock_session_cm.__exit__ = MagicMock(return_value=None)
            mock_get_session_context.return_value = mock_session_cm

            # Act
            result = delete_task_mcp(user_id, task_id)

            # Assert
            assert result["status"] == "error"
            assert "Failed to delete task" in result["message"]

    def test_delete_task_validation_error_handling(self):
        """Test that validation errors are properly handled."""
        # Arrange
        invalid_user_id = "invalid-uuid"
        invalid_task_id = "also-invalid-uuid"

        # Act & Assert
        result = delete_task_mcp(invalid_user_id, invalid_task_id)
        assert result["status"] == "error"
        assert "Invalid user ID format" in result["message"]