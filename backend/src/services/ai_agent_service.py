from typing import Dict, Any, List
from ..models.message import Message
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def process_message(messages: List[Dict[str, str]], user_id: str) -> Dict[str, Any]:
    """
    Process a message with the AI agent and return the response

    Args:
        messages: List of message dictionaries with 'role' and 'content' keys
        user_id: User ID for context

    Returns:
        Dictionary containing the AI response and any tool calls
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo",  # or gpt-3.5-turbo
            messages=messages,
            temperature=0.7
        )

        ai_response = response.choices[0].message.content
        tool_calls = response.choices[0].message.tool_calls or []

        # Convert tool calls to the format expected by the API
        tool_calls_formatted = []
        if tool_calls:
            for tool_call in tool_calls:
                tool_calls_formatted.append({
                    "id": tool_call.id,
                    "type": tool_call.type,
                    "function": {
                        "name": tool_call.function.name,
                        "arguments": tool_call.function.arguments
                    }
                })

        return {
            "content": ai_response,
            "role": "assistant",
            "tool_calls": tool_calls_formatted
        }
    except Exception as e:
        # In a real implementation, we'd have more sophisticated error handling
        raise Exception(f"AI service error: {str(e)}")


def format_conversation_for_ai(messages: List[Message]) -> List[Dict[str, str]]:
    """
    Format conversation history for AI processing
    """
    formatted_messages = []
    for msg in messages:
        formatted_messages.append({
            "role": msg.role,
            "content": msg.content
        })
    return formatted_messages