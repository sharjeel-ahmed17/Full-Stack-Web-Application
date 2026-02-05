"""
Tests for add_task MCP tool

This module contains tests for the add_task functionality in the MCP tools.
"""
import pytest
from unittest.mock import patch, MagicMock
from uuid import uuid4, UUID
from src.mcp.tools.task_operations import create_task_mcp
from src.mcp.tools.validators import TaskValidator


class TestAddTask:
    """Test class for add_task functionality."""

    def test_add_task_valid_input(self):
        """Test add_task with valid input successfully creates task."""
        # Arrange
        user_id = str(uuid4())
        title = "Test Task"
        description = "Test Description"

        # Mock the database session and service
        mock_session = MagicMock()
        mock_task = MagicMock()
        mock_task.id = uuid4()
        mock_task.title = title

        with patch('src.mcp.tools.task_operations.get_session') as mock_get_session_context:
            mock_session_cm = MagicMock()
            mock_session_cm.__enter__ = MagicMock(return_value=mock_session)
            mock_session_cm.__exit__ = MagicMock(return_value=None)
            mock_get_session_context.return_value = mock_session_cm

            with patch('src.mcp.tools.task_operations.service_create_task', return_value=mock_task) as mock_service:

                # Act
                result = create_task_mcp(user_id, title, description)

                # Assert
                assert result["status"] == "success"
                assert result["message"] == f"Task '{title}' created successfully"
                mock_service.assert_called_once()

    def test_add_task_invalid_user_id(self):
        """Test add_task with invalid user ID returns error."""
        # Arrange
        invalid_user_id = "invalid-uuid"
        title = "Test Task"

        # Act
        result = create_task_mcp(invalid_user_id, title)

        # Assert
        assert result["status"] == "error"
        assert "Invalid user ID format" in result["message"]

    def test_add_task_empty_title(self):
        """Test add_task with empty title returns error."""
        # Arrange
        user_id = str(uuid4())
        title = ""

        # Act
        result = create_task_mcp(user_id, title)

        # Assert
        assert result["status"] == "error"
        assert "Task title cannot be empty" in result["message"]

    def test_add_task_whitespace_only_title(self):
        """Test add_task with whitespace-only title returns error."""
        # Arrange
        user_id = str(uuid4())
        title = "   "

        # Act
        result = create_task_mcp(user_id, title)

        # Assert
        assert result["status"] == "error"
        assert "Task title cannot be empty" in result["message"]

    def test_add_task_long_title(self):
        """Test add_task with too long title returns error."""
        # Arrange
        user_id = str(uuid4())
        title = "A" * 201  # Exceeds 200 character limit

        # Act
        result = create_task_mcp(user_id, title)

        # Assert
        assert result["status"] == "error"
        assert "Task title must be 200 characters or less" in result["message"]

    def test_add_task_valid_with_description(self):
        """Test add_task with valid input including description."""
        # Arrange
        user_id = str(uuid4())
        title = "Test Task"
        description = "This is a test description that can be fairly long"

        # Mock the database session and service
        mock_session = MagicMock()
        mock_task = MagicMock()
        mock_task.id = uuid4()
        mock_task.title = title

        with patch('src.mcp.tools.task_operations.get_session') as mock_get_session_context:
            mock_session_cm = MagicMock()
            mock_session_cm.__enter__ = MagicMock(return_value=mock_session)
            mock_session_cm.__exit__ = MagicMock(return_value=None)
            mock_get_session_context.return_value = mock_session_cm

            with patch('src.mcp.tools.task_operations.service_create_task', return_value=mock_task) as mock_service:

                # Act
                result = create_task_mcp(user_id, title, description)

                # Assert
                assert result["status"] == "success"
                assert result["message"] == f"Task '{title}' created successfully"
                mock_service.assert_called_once()

    def test_add_task_too_long_description(self):
        """Test add_task with too long description returns error."""
        # Arrange
        user_id = str(uuid4())
        title = "Test Task"
        description = "A" * 1001  # Exceeds 1000 character limit

        # Act
        result = create_task_mcp(user_id, title, description)

        # Assert
        assert result["status"] == "error"
        assert "Task description must be 1000 characters or less" in result["message"]

    def test_add_task_database_error(self):
        """Test add_task handles database errors gracefully."""
        # Arrange
        user_id = str(uuid4())
        title = "Test Task"

        with patch('src.mcp.tools.task_operations.get_session') as mock_get_session_context:
            mock_session_cm = MagicMock()
            mock_session_cm.__enter__ = MagicMock(side_effect=Exception("DB Connection failed"))
            mock_session_cm.__exit__ = MagicMock(return_value=None)
            mock_get_session_context.return_value = mock_session_cm

            # Act
            result = create_task_mcp(user_id, title)

            # Assert
            assert result["status"] == "error"
            assert "Failed to create task" in result["message"]

    def test_add_task_validation_error_handling(self):
        """Test that validation errors are properly handled."""
        # Arrange
        user_id = str(uuid4())
        title = ""  # Invalid title

        # Act & Assert
        result = create_task_mcp(user_id, title)
        assert result["status"] == "error"
        assert "Task title cannot be empty" in result["message"]