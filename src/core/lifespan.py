from contextlib import asynccontextmanager
from supabase import create_async_client
from src.core.config import settings
from src.core.log import Logger
from src.repositories import ConversationRepository, MessageRepository, UserRepository, PlanRepository, PlayerRepository, LogRepository
from src.services.llm_service import LlmService

@asynccontextmanager
async def lifespan(app):
    supabase = await create_async_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
    
    app.state.conversation_repo = ConversationRepository(supabase)
    app.state.message_repo = MessageRepository(supabase)
    app.state.user_repo = UserRepository(supabase)
    app.state.plan_repo = PlanRepository(supabase)
    app.state.player_repo = PlayerRepository(supabase)

    app.state.log_repo = LogRepository(supabase)
    app.state.logger = Logger(app.state.log_repo)

    # app.state.llm_service = LlmService(settings.GEMINI_API_KEY, app.state.logger)
    # app.state.movefile_service = MoveFileService(settings.N8N_MOVE_WEBHOOK_URL, app.state.logger, headers={"HEADER_AUTH_KEY": settings.HEADER_AUTH_KEY})

    # Force contain API key in settings
    assert settings.HEADER_AUTH_KEY, "HEADER_AUTH_KEY must be set in settings"
    yield