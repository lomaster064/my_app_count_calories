from datetime import date
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class InjuryCreate(BaseModel):
    injury_type: str
    description: Optional[str] = None
    restricted_exercises: list[str] = Field(default_factory=list)


class UserBase(BaseModel):
    email: EmailStr
    name: str
    gender: Optional[str] = None
    birth_date: Optional[date] = None
    height_cm: float
    current_weight_kg: float
    target_weight_kg: float
    goal: str
    activity_level: str
    training_level: str
    allergies: list[str] = Field(default_factory=list)
    intolerances: list[str] = Field(default_factory=list)
    diet_type: Optional[str] = None
    dislikes: list[str] = Field(default_factory=list)
    meals_per_day: int = 3
    meal_time_preferences: list[str] = Field(default_factory=list)


class UserCreate(UserBase):
    password: str
    injuries: list[InjuryCreate] = Field(default_factory=list)


class UserUpdate(BaseModel):
    name: Optional[str] = None
    gender: Optional[str] = None
    birth_date: Optional[date] = None
    height_cm: Optional[float] = None
    current_weight_kg: Optional[float] = None
    target_weight_kg: Optional[float] = None
    goal: Optional[str] = None
    activity_level: Optional[str] = None
    training_level: Optional[str] = None
    allergies: Optional[list[str]] = None
    intolerances: Optional[list[str]] = None
    diet_type: Optional[str] = None
    dislikes: Optional[list[str]] = None
    meals_per_day: Optional[int] = None
    meal_time_preferences: Optional[list[str]] = None


class UserOut(UserBase):
    id: int

    class Config:
        from_attributes = True
