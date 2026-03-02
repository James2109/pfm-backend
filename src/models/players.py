from typing import Optional
from pydantic import BaseModel, ConfigDict
from enum import Enum
from datetime import datetime


class League(Enum):
    PREMIER_LEAGUE = "Premier League"
    BUNDESLIGA = "Bundesliga"
    SERIE_A = "Serie A"
    LA_LIGA = "La Liga"
    LIGUE_1 = "Ligue 1"


class Position(Enum):
    GOALKEEPER = "Goalkeeper"

    CENTER_BACK = "Center Back"
    LEFT_BACK = "Left Back"
    RIGHT_BACK = "Right Back"
    WING_BACK = "Wing Back"
    SWEEPER = "Sweeper"

    DEFENSIVE_MIDFIELDER = "Defensive Midfielder"
    CENTER_MIDFIELDER = "Center Midfielder"
    ATTACKING_MIDFIELDER = "Attacking Midfielder"
    LEFT_MIDFIELDER = "Left Midfielder"
    RIGHT_MIDFIELDER = "Right Midfielder"

    STRIKER = "Striker"
    CENTER_FORWARD = "Center Forward"
    LEFT_WINGER = "Left Winger"
    RIGHT_WINGER = "Right Winger"
    SECOND_STRIKER = "Second Striker"


class Evaluation(Enum):
    ONE_STAR = 1
    TWO_STARS = 2
    THREE_STARS = 3
    FOUR_STARS = 4
    FIVE_STARS = 5


class Player(BaseModel):
    id: str
    avatar_id: str
    name: str
    age: int
    nationality: str
    league: League
    club: str
    position: Position
    shirt_number: int
    height: float
    weight: float
    right_foot: Evaluation
    left_foot: Evaluation
    skill: Evaluation
    appearances: int
    minutes_played: int
    goals: int
    assists: int
    clearances: int
    yellow_cards: int
    red_cards: int
    max_speed: float
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class PlayerCreate(BaseModel):
    avatar_id: str
    name: str
    age: int
    nationality: str
    league: League
    club: str
    position: Position
    shirt_number: int
    height: float
    weight: float
    right_foot: Evaluation
    left_foot: Evaluation
    skill: Evaluation
    appearances: int
    minutes_played: int
    goals: int
    assists: int
    clearances: int
    yellow_cards: int
    red_cards: int
    max_speed: float


class PlayerUpdate(BaseModel):
    avatar_id: Optional[str] = None
    name: Optional[str] = None
    age: Optional[int] = None
    nationality: Optional[str] = None
    league: Optional[League] = None
    club: Optional[str] = None
    position: Optional[Position] = None
    shirt_number: Optional[int] = None
    height: Optional[float] = None
    weight: Optional[float] = None
    right_foot: Optional[Evaluation] = None
    left_foot: Optional[Evaluation] = None
    skill: Optional[Evaluation] = None
    appearances: Optional[int] = None
    minutes_played: Optional[int] = None
    goals: Optional[int] = None
    assists: Optional[int] = None
    clearances: Optional[int] = None
    yellow_cards: Optional[int] = None
    red_cards: Optional[int] = None
    max_speed: Optional[float] = None