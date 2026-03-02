from typing import Optional
from pydantic import BaseModel, ConfigDict
from enum import Enum
from datetime import datetime


class MessageFrom(Enum):
    BOT = "bot"
    HUMAN = "human"


class Message(BaseModel):
    id: str
    conversation_id: str
    message_from: MessageFrom
    message: str
    reason: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class MessageCreate(BaseModel):
    conversation_id: str
    message_from: MessageFrom
    message: str
    reason: Optional[str] = None