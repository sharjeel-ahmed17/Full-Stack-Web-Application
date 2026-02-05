from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """Configuration settings for AI agent integration."""

    # OpenAI settings
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview")

    # Database settings
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./test.db")

    # Application settings
    app_name: str = "AI Agent Integration"
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"
    api_v1_prefix: str = "/api/v1"

    # AI Agent settings
    ai_agent_max_tokens: int = 1000
    ai_agent_temperature: float = 0.7
    ai_agent_timeout: int = 30  # seconds

    # MCP Tool settings
    mcp_server_url: str = os.getenv("MCP_SERVER_URL", "http://localhost:8080")

    # Conversation settings
    max_conversation_length: int = 100  # maximum number of messages in a conversation
    conversation_ttl_hours: int = 24  # time to live for conversations in hours

    class Config:
        env_file = ".env"


settings = Settings()