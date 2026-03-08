from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from src.repositories import MessageRepository
from src.models.messages import Message, MessageCreate
from src.core.dependencies import get_message_repo, get_current_user

router = APIRouter(prefix="/messages", tags=["Messages"], dependencies=[Depends(get_current_user)])

@router.get("/", response_model=List[Message])
async def get_all_messages(repo: MessageRepository = Depends(get_message_repo)):
    messages = await repo.get_all()
    if not messages:
        raise HTTPException(status_code=404, detail="No messages found")
    return messages

@router.get("/{message_id}", response_model=Message)
async def get_message_by_id(
    message_id: str,
    repo: MessageRepository = Depends(get_message_repo),
):
    message = await repo.get_by_id(message_id)
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    return message


@router.get("/conversation/{conversation_id}", response_model=List[Message])
async def get_messages_by_conversation(
    conversation_id: str,
    repo: MessageRepository = Depends(get_message_repo),
):
    messages = await repo.get_by_conversation_id(conversation_id)
    if not messages:
        raise HTTPException(status_code=404, detail="No messages found")
    return messages


@router.post("/", response_model=Message, status_code=status.HTTP_201_CREATED)
async def create_message(
    data: MessageCreate,
    repo: MessageRepository = Depends(get_message_repo),
):
    result = await repo.create(data)
    if not result:
        raise HTTPException(status_code=400, detail="Failed to create message")
    return result


@router.delete("/{message_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_message(
    message_id: str,
    repo: MessageRepository = Depends(get_message_repo),
):
    success = await repo.delete(message_id)
    if not success:
        raise HTTPException(status_code=404, detail="Message not found")
