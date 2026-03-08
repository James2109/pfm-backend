from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime


class User(BaseModel):
    id: str
    first_name: str
    last_name: str
    full_name: str
    phone_number: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    full_name: Optional[str] = None
    phone_number: Optional[str] = None
