from typing import Optional
from pydantic import BaseModel, ConfigDict
from enum import Enum
from datetime import datetime
from src.models.players import Position


class Frequency(Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"


class Plan(BaseModel):
    id: str
    plan_name: str
    user_id: str
    age: int
    position: Position
    height: float
    weight: float
    strength: str
    weakness: str
    note: str
    frequency: Frequency
    training_sessions: int
    cost_per_meal: float
    nutrition_plan: str
    training_plan: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class PlanCreate(BaseModel):
    plan_name: str
    user_id: str
    age: int
    position: Position
    height: float
    weight: float
    strength: str
    weakness: str
    note: str
    frequency: Frequency
    training_sessions: int
    cost_per_meal: float
    nutrition_plan: str
    training_plan: str


class PlanUpdate(BaseModel):
    plan_name: Optional[str] = None
    age: Optional[int] = None
    position: Optional[Position] = None
    height: Optional[float] = None
    weight: Optional[float] = None
    strength: Optional[str] = None
    weakness: Optional[str] = None
    note: Optional[str] = None
    frequency: Optional[Frequency] = None
    training_sessions: Optional[int] = None
    cost_per_meal: Optional[float] = None
    nutrition_plan: Optional[str] = None
    training_plan: Optional[str] = None