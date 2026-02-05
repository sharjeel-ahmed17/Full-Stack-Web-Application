import asyncio
import logging
from typing import Dict, Any, Optional
from uuid import UUID
from openai import OpenAI
import re
from ..models.conversation import Conversation
from ..models.message import Message
from ..models.ai_interaction import AIInteraction
from ..services.conversation_service import ConversationService
from ..services.message_service import MessageService
from ..services.ai_interaction_service import AIInteractionService
from ..core.config import settings
from ..core.security import validate_ai_input
from ..tools.mcp_tools import mcp_task_tools


logger = logging.getLogger(__name__)


class AIAgentService:
    """Service for orchestrating AI agent interactions with MCP tools."""

    def __init__(self):
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.conversation_service = ConversationService()
        self.message_service = MessageService()
        self.ai_interaction_service = AIInteractionService()
        self.mcp_tools = mcp_task_tools
        self.logger = logging.getLogger(__name__)

    async def process_user_message(self, session, conversation_id: UUID, user_message: str) -> Dict[str, Any]:
        """
        Process a user message through the AI agent and return the response.

        Args:
            session: Database session
            conversation_id: ID of the conversation
            user_message: The user's natural language message

        Returns:
            Dict containing the AI response and any tool calls made
        """
        # Validate input for security
        if not validate_ai_input(user_message):
            return {
                "response": "Invalid input received. Please try again with appropriate content.",
                "conversation_id": str(conversation_id),
                "tool_calls": []
            }

        # Add user message to conversation
        user_msg = self.message_service.create_message(
            session=session,
            conversation_id=conversation_id,
            role="user",
            content=user_message
        )

        # Get the conversation to access user_id
        conversation = self.conversation_service.get_conversation(session, conversation_id)
        if not conversation:
            return {
                "response": "Conversation not found.",
                "conversation_id": str(conversation_id),
                "tool_calls": []
            }

        # Try to extract task operations from the user message
        tool_calls = []
        ai_response = ""

        # Check if the message is a task-related command
        task_operations = self._identify_task_operations(user_message, conversation.user_id)

        if task_operations:
            # Process the identified task operations
            for operation in task_operations:
                try:
                    if operation['operation'] == 'add':
                        result = self.mcp_tools.add_task(
                            user_id=str(conversation.user_id),
                            title=operation['title'],
                            description=operation.get('description', '')
                        )
                        tool_calls.append({
                            "tool_name": "add_task",
                            "result": result
                        })

                        # Create AI interaction record
                        self.ai_interaction_service.create_interaction(
                            session=session,
                            conversation_id=conversation_id,
                            tool_name="add_task",
                            input_params={"title": operation['title'], "description": operation.get('description', '')},
                            output_result=result,
                            success=result.get('success', False)
                        )

                        ai_response = result.get('message', 'Task added successfully.')

                    elif operation['operation'] == 'list':
                        status_filter = operation.get('status', 'all')
                        result = self.mcp_tools.list_tasks(
                            user_id=str(conversation.user_id),
                            status=status_filter
                        )
                        tool_calls.append({
                            "tool_name": "list_tasks",
                            "result": result
                        })

                        # Create AI interaction record
                        self.ai_interaction_service.create_interaction(
                            session=session,
                            conversation_id=conversation_id,
                            tool_name="list_tasks",
                            input_params={"status": status_filter},
                            output_result=result,
                            success=result.get('success', False)
                        )

                        if result.get('success'):
                            tasks = result.get('tasks', [])
                            if tasks:
                                task_list = "\n".join([f"- {task.get('title', 'Unknown')}" for task in tasks])
                                ai_response = f"Here are your tasks:\n{task_list}"
                            else:
                                ai_response = f"You don't have any {status_filter} tasks."
                        else:
                            ai_response = f"Sorry, I couldn't retrieve your tasks: {result.get('error', 'Unknown error')}"

                    elif operation['operation'] == 'update':
                        result = self.mcp_tools.update_task(
                            user_id=str(conversation.user_id),
                            task_id=operation['task_id'],
                            title=operation.get('title'),
                            description=operation.get('description'),
                            is_completed=operation.get('is_completed')
                        )
                        tool_calls.append({
                            "tool_name": "update_task",
                            "result": result
                        })

                        # Create AI interaction record
                        self.ai_interaction_service.create_interaction(
                            session=session,
                            conversation_id=conversation_id,
                            tool_name="update_task",
                            input_params={
                                "task_id": operation['task_id'],
                                "title": operation.get('title'),
                                "description": operation.get('description'),
                                "is_completed": operation.get('is_completed')
                            },
                            output_result=result,
                            success=result.get('success', False)
                        )

                        ai_response = result.get('message', 'Task updated successfully.')

                    elif operation['operation'] == 'delete':
                        result = self.mcp_tools.delete_task(
                            user_id=str(conversation.user_id),
                            task_id=operation['task_id']
                        )
                        tool_calls.append({
                            "tool_name": "delete_task",
                            "result": result
                        })

                        # Create AI interaction record
                        self.ai_interaction_service.create_interaction(
                            session=session,
                            conversation_id=conversation_id,
                            tool_name="delete_task",
                            input_params={"task_id": operation['task_id']},
                            output_result=result,
                            success=result.get('success', False)
                        )

                        ai_response = result.get('message', 'Task deleted successfully.')

                    elif operation['operation'] == 'complete':
                        result = self.mcp_tools.complete_task(
                            user_id=str(conversation.user_id),
                            task_id=operation['task_id']
                        )
                        tool_calls.append({
                            "tool_name": "complete_task",
                            "result": result
                        })

                        # Create AI interaction record
                        self.ai_interaction_service.create_interaction(
                            session=session,
                            conversation_id=conversation_id,
                            tool_name="complete_task",
                            input_params={"task_id": operation['task_id']},
                            output_result=result,
                            success=result.get('success', False)
                        )

                        ai_response = result.get('message', 'Task completed successfully.')

                except Exception as e:
                    error_result = {
                        "success": False,
                        "error": f"Error executing {operation['operation']} operation: {str(e)}"
                    }

                    # Create AI interaction record for error
                    self.ai_interaction_service.create_interaction(
                        session=session,
                        conversation_id=conversation_id,
                        tool_name=f"{operation['operation']}_task",
                        input_params=operation,
                        output_result=error_result,
                        success=False
                    )

                    tool_calls.append({
                        "tool_name": f"{operation['operation']}_task",
                        "result": error_result
                    })
                    ai_response = f"Sorry, I encountered an error: {str(e)}"

        else:
            # If no specific task operations, just use the AI for general response
            # Prepare the conversation history for the AI
            messages = self.conversation_service.get_conversation_messages(session, conversation_id)
            ai_messages = [
                {"role": msg.role, "content": msg.content}
                for msg in messages
            ]

            # Add the user's message to the conversation
            ai_messages.append({"role": "user", "content": user_message})

            try:
                # Call the OpenAI API with the conversation history
                response = self.client.chat.completions.create(
                    model=settings.openai_model,
                    messages=ai_messages,
                    max_tokens=settings.ai_agent_max_tokens,
                    temperature=settings.ai_agent_temperature,
                )

                # Extract the AI response
                ai_response = response.choices[0].message.content

            except Exception as e:
                ai_response = f"I encountered an error processing your request: {str(e)}"

        # Add AI response to conversation
        ai_msg = self.message_service.create_message(
            session=session,
            conversation_id=conversation_id,
            role="assistant",
            content=ai_response
        )

        # Update conversation timestamp
        self.conversation_service.update_conversation_title(
            session, conversation_id, f"Conversation {conversation.created_at.strftime('%Y-%m-%d %H:%M')}"
        )

        return {
            "response": ai_response,
            "conversation_id": str(conversation_id),
            "tool_calls": tool_calls
        }

    def _identify_task_operations(self, user_message: str, user_id: UUID) -> list:
        """
        Identify task operations from user message using pattern matching.

        Args:
            user_message: The user's message
            user_id: The user ID

        Returns:
            List of operations to perform
        """
        operations = []

        # Convert to lowercase for easier matching
        lower_msg = user_message.lower().strip()

        # Add task patterns
        add_patterns = [
            r"add a task to (.+?)(?:$|\.)",
            r"create a task to (.+?)(?:$|\.)",
            r"add task (.+?)(?:$|\.)",
            r"create task (.+?)(?:$|\.)",
        ]

        for pattern in add_patterns:
            matches = re.findall(pattern, lower_msg)
            for match in matches:
                # Clean up the task title
                title = match.strip()
                if title:
                    operations.append({
                        "operation": "add",
                        "title": title.capitalize()
                    })

        # List tasks patterns
        list_patterns = [
            r"show me my (pending|completed)?\s*task",
            r"list my (pending|completed)?\s*task",
            r"what are my (pending|completed)?\s*tasks?",
            r"show tasks?",
            r"list tasks?"
        ]

        for pattern in list_patterns:
            matches = re.findall(pattern, lower_msg)
            for match in matches:
                status = match.strip() if match.strip() else "all"
                operations.append({
                    "operation": "list",
                    "status": status if status in ["pending", "completed"] else "all"
                })

        # Complete task patterns
        complete_patterns = [
            r"mark.*?as complete",
            r"complete.*?task",
            r"finish.*?task",
            r"done with.*?task"
        ]

        for pattern in complete_patterns:
            if re.search(pattern, lower_msg):
                # Extract task title if possible
                # This is a simplified approach - in a real system, you'd have more robust NER
                operations.append({
                    "operation": "complete",
                    "task_id": "unknown"  # Would need to implement task lookup in real system
                })

        # Update task patterns
        update_patterns = [
            r"update.*?task",
            r"change.*?task",
            r"edit.*?task"
        ]

        for pattern in update_patterns:
            if re.search(pattern, lower_msg):
                operations.append({
                    "operation": "update",
                    "task_id": "unknown"
                })

        # Delete task patterns
        delete_patterns = [
            r"delete.*?task",
            r"remove.*?task"
        ]

        for pattern in delete_patterns:
            if re.search(pattern, lower_msg):
                operations.append({
                    "operation": "delete",
                    "task_id": "unknown"
                })

        return operations

    def _format_error_response(self, error_message: str) -> str:
        """
        Format error messages for user-friendly responses.

        Args:
            error_message: The raw error message

        Returns:
            User-friendly error message
        """
        # Map technical errors to user-friendly messages
        if "connection error" in error_message.lower():
            return "I'm currently unable to connect to the task management system. Please try again in a moment."
        elif "timeout" in error_message.lower():
            return "The system took too long to respond. Please try your request again."
        elif "invalid" in error_message.lower() or "empty" in error_message.lower():
            return f"I couldn't process your request: {error_message}"
        elif "not found" in error_message.lower():
            return "I couldn't find what you were looking for. Could you please rephrase your request?"
        else:
            return f"I encountered an issue while processing your request. {error_message}"

    async def create_new_conversation(self, session, user_id: UUID) -> Conversation:
        """Create a new conversation for a user."""
        return self.conversation_service.create_conversation(session, user_id)

    async def get_conversation_history(self, session, conversation_id: UUID) -> Dict[str, Any]:
        """Get the full conversation history."""
        conversation = self.conversation_service.get_conversation(session, conversation_id)
        if not conversation:
            return {}

        messages = self.conversation_service.get_conversation_messages(session, conversation_id)

        return {
            "id": str(conversation.id),
            "title": conversation.title,
            "created_at": conversation.created_at.isoformat(),
            "updated_at": conversation.updated_at.isoformat(),
            "messages": [
                {
                    "id": str(msg.id),
                    "role": msg.role,
                    "content": msg.content,
                    "timestamp": msg.timestamp.isoformat()
                }
                for msg in messages
            ]
        }