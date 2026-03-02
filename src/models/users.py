from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime


class User(BaseModel):
    id: str
    username: str
    hashed_password: str
    first_name: str
    last_name: str
    full_name: str
    email: str
    phone_number: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    username: str
    password: str
    first_name: str
    last_name: str
    full_name: str
    email: str
    phone_number: Optional[str] = None


class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    full_name: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None


class UserPasswordUpdate(BaseModel):
    password: str


class UserResponse(BaseModel):
    id: str
    username: str
    first_name: str
    last_name: str
    full_name: str
    email: str
    phone_number: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
