from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from src.repositories import ConversationRepository
from src.models.conversations import Conversation, ConversationCreate
from src.models.messages import ChatRequest, ChatResponse
from src.services.chat_service import ChatService
from src.core.dependencies import get_conversation_repo, get_chat_service, get_current_user

router = APIRouter(prefix="/conversations", tags=["Conversations"], dependencies=[Depends(get_current_user)])


@router.get("/", response_model=List[Conversation])
async def get_all_conversations(repo: ConversationRepository = Depends(get_conversation_repo)):
    conversations = await repo.get_all()
    if not conversations:
        raise HTTPException(status_code=404, detail="No conversations found")
    return conversations


@router.get("/{conversation_id}", response_model=Conversation)
async def get_conversation_by_id(
    conversation_id: str,
    repo: ConversationRepository = Depends(get_conversation_repo),
):
    conversation = await repo.get_by_id(conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation


@router.get("/user/{user_id}", response_model=List[Conversation])
async def get_conversations_by_user(
    user_id: str,
    repo: ConversationRepository = Depends(get_conversation_repo),
):
    conversations = await repo.get_by_user_id(user_id)
    if not conversations:
        raise HTTPException(status_code=404, detail="No conversations found")
    return conversations


@router.post("/", response_model=Conversation, status_code=status.HTTP_201_CREATED)
async def create_conversation(
    data: ConversationCreate,
    repo: ConversationRepository = Depends(get_conversation_repo),
):
    result = await repo.create(data)
    if not result:
        raise HTTPException(status_code=400, detail="Failed to create conversation")
    return result


@router.post("/chat", response_model=ChatResponse)
async def chat(
    data: ChatRequest,
    current_user: dict = Depends(get_current_user),
    chat_service: ChatService = Depends(get_chat_service),
):
    return await chat_service.chat(
        user_message=data.message,
        user_id=current_user["user_id"],
        conversation_id=data.conversation_id,
    )


@router.delete("/{conversation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_conversation(
    conversation_id: str,
    repo: ConversationRepository = Depends(get_conversation_repo),
):
    success = await repo.delete(conversation_id)
    if not success:
        raise HTTPException(status_code=404, detail="Conversation not found")
