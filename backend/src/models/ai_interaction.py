from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional, Dict, Any
from sqlmodel import Field, SQLModel


class AIInteractionBase(SQLModel):
    conversation_id: UUID
    tool_name: str  # Name of the MCP tool called
    input_params: Dict[str, Any]  # Parameters passed to the tool
    output_result: Dict[str, Any]  # Result returned from the tool
    timestamp: Optional[datetime] = Field(default_factory=datetime.utcnow)
    success: bool = True  # Whether the interaction succeeded


class AIInteraction(AIInteractionBase, table=True):
    """
    AIInteraction model representing interactions between AI agent and MCP tools.

    Validation rules:
    - Conversation_id must reference existing conversation
    - Tool_name must be valid registered tool
    - Success flag must match presence of error in output
    """
    id: UUID = Field(default_factory=uuid4, primary_key=True)


class AIInteractionCreate(AIInteractionBase):
    pass


class AIInteractionRead(AIInteractionBase):
    id: UUID