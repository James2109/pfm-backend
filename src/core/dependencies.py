from fastapi import Request, Header, HTTPException
from src.repositories import ConversationRepository, MessageRepository, UserRepository, PlanRepository, PlayerRepository, LogRepository
from src.core.config import settings

def get_conversation_repo(request: Request) -> ConversationRepository:
    return request.app.state.conversation_repo

def get_message_repo(request: Request) -> MessageRepository:
    return request.app.state.message_repo

def get_user_repo(request: Request) -> UserRepository:
    return request.app.state.user_repo

def get_plan_repo(request: Request) -> PlanRepository:
    return request.app.state.plan_repo

def get_player_repo(request: Request) -> PlayerRepository:
    return request.app.state.player_repo

def get_gemini_service(request: Request):
    return request.app.state.gemini_service

def get_logger(request: Request) -> LogRepository:
    return request.app.state.logger

async def verify_api_key(x_api_key: str = Header(...)):
    """
    Verify API key from X-API-Key header.
    If API_KEY is not configured, authentication is disabled.
    """
    # Check if header is provided
    if not x_api_key:
        raise HTTPException(
            status_code=401,
            detail="Missing API Key. Provide X-API-Key header."
        )

    # Validate the key
    if x_api_key != settings.HEADER_AUTH_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid API Key"
        )