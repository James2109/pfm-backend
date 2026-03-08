from fastapi import Request, Header, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.repositories import ConversationRepository, MessageRepository, UserRepository, PlanRepository, PlayerRepository, LogRepository
from src.core.config import settings
from src.core.security import decode_supabase_token
import jwt

bearer_scheme = HTTPBearer()

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

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)) -> dict:
    try:
        payload = decode_supabase_token(credentials.credentials)
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token: missing user ID")
        return {"user_id": user_id, "email": payload.get("email")}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

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