from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime


class Conversation(BaseModel):
    id: str
    user_id: str
    title: str
    message_count: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class ConversationCreate(BaseModel):
    user_id: str
    title: str


class ConversationUpdate(BaseModel):
    title: str