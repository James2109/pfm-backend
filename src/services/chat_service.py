from typing import Optional

from src.models.messages import MessageCreate, MessageFrom, ChatResponse
from src.models.conversations import ConversationCreate
from src.repositories import ConversationRepository, MessageRepository, PlayerRepository, PlanRepository
from src.services.agent_service import AgentService


class ChatService:
    def __init__(
        self,
        conversation_repo: ConversationRepository,
        message_repo: MessageRepository,
        player_repo: PlayerRepository,
        plan_repo: PlanRepository,
        agent: AgentService,
    ):
        self.conversation_repo = conversation_repo
        self.message_repo = message_repo
        self.player_repo = player_repo
        self.plan_repo = plan_repo
        self.agent = agent

    async def chat(
        self,
        user_message: str,
        user_id: str,
        conversation_id: Optional[str] = None,
    ) -> ChatResponse:
        # Auto-create conversation if not provided
        if not conversation_id:
            title = user_message[:50] + ("..." if len(user_message) > 50 else "")
            conversation = await self.conversation_repo.create(
                ConversationCreate(user_id=user_id, title=title)
            )
            conversation_id = conversation["id"]

        # Get conversation history
        history = await self.message_repo.get_by_conversation_id(conversation_id)
        if not history:
            history = []

        # Save user message
        user_msg = await self.message_repo.create(MessageCreate(
            conversation_id=conversation_id,
            message_from=MessageFrom.HUMAN,
            message=user_message,
        ))

        # Run agent
        bot_response = await self.agent.chat(
            user_message=user_message,
            conversation_history=history,
            player_repo=self.player_repo,
            plan_repo=self.plan_repo,
            user_id=user_id,
        )

        # Save bot message
        bot_msg = await self.message_repo.create(MessageCreate(
            conversation_id=conversation_id,
            message_from=MessageFrom.BOT,
            message=bot_response,
        ))

        # Update message count
        await self.conversation_repo.update_message_count(conversation_id, len(history) + 2)

        return ChatResponse(
            conversation_id=conversation_id,
            user_message=user_msg,
            bot_message=bot_msg,
        )
