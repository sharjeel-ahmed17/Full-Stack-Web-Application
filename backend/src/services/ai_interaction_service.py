import logging
from typing import Optional, List, Dict, Any
from uuid import UUID
from sqlmodel import Session, select
from ..models.ai_interaction import AIInteraction, AIInteractionCreate


class AIInteractionService:
    """Service for managing AI agent interactions with MCP tools."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def create_interaction(self, session: Session, conversation_id: UUID, tool_name: str,
                         input_params: Dict[str, Any], output_result: Dict[str, Any],
                         success: bool = True) -> AIInteraction:
        """Create a new AI interaction record."""
        try:
            interaction = AIInteraction(
                conversation_id=conversation_id,
                tool_name=tool_name,
                input_params=input_params,
                output_result=output_result,
                success=success
            )
            session.add(interaction)
            session.commit()
            session.refresh(interaction)

            # Log the interaction
            self.logger.info(f"Created AI interaction: {tool_name} for conversation {conversation_id}")

            return interaction
        except Exception as e:
            self.logger.error(f"Error creating AI interaction: {str(e)}")
            raise

    def get_interaction(self, session: Session, interaction_id: UUID) -> Optional[AIInteraction]:
        """Retrieve an interaction by ID."""
        try:
            statement = select(AIInteraction).where(AIInteraction.id == interaction_id)
            interaction = session.exec(statement).first()

            if interaction:
                self.logger.debug(f"Retrieved interaction {interaction_id}")
            else:
                self.logger.warning(f"Interaction {interaction_id} not found")

            return interaction
        except Exception as e:
            self.logger.error(f"Error retrieving interaction {interaction_id}: {str(e)}")
            raise

    def get_interactions_by_conversation(self, session: Session, conversation_id: UUID) -> List[AIInteraction]:
        """Retrieve all interactions for a conversation."""
        try:
            statement = select(AIInteraction).where(AIInteraction.conversation_id == conversation_id).order_by(AIInteraction.timestamp)
            interactions = session.exec(statement).all()

            self.logger.info(f"Retrieved {len(interactions)} interactions for conversation {conversation_id}")

            return interactions
        except Exception as e:
            self.logger.error(f"Error retrieving interactions for conversation {conversation_id}: {str(e)}")
            raise

    def get_interactions_by_tool(self, session: Session, conversation_id: UUID, tool_name: str) -> List[AIInteraction]:
        """Retrieve all interactions for a specific tool in a conversation."""
        try:
            statement = select(AIInteraction).where(
                AIInteraction.conversation_id == conversation_id,
                AIInteraction.tool_name == tool_name
            ).order_by(AIInteraction.timestamp)
            interactions = session.exec(statement).all()

            self.logger.info(f"Retrieved {len(interactions)} interactions for tool '{tool_name}' in conversation {conversation_id}")

            return interactions
        except Exception as e:
            self.logger.error(f"Error retrieving interactions for tool '{tool_name}' in conversation {conversation_id}: {str(e)}")
            raise

    def update_interaction_result(self, session: Session, interaction_id: UUID,
                                output_result: Dict[str, Any], success: bool) -> Optional[AIInteraction]:
        """Update interaction result and success status."""
        try:
            interaction = self.get_interaction(session, interaction_id)
            if interaction:
                interaction.output_result = output_result
                interaction.success = success
                session.add(interaction)
                session.commit()
                session.refresh(interaction)

                self.logger.info(f"Updated interaction {interaction_id} with success={success}")

            return interaction
        except Exception as e:
            self.logger.error(f"Error updating interaction {interaction_id}: {str(e)}")
            raise