from datetime import date

from pydantic import BaseModel, Field


class MealLogItemIn(BaseModel):
    name: str
    grams_estimate: float
    calories: float
    protein: float
    fat: float
    carbs: float
    confidence: float


class MealLogIn(BaseModel):
    logged_date: date
    notes: str = ""
    items: list[MealLogItemIn] = Field(default_factory=list)


class MealLogItemOut(MealLogItemIn):
    id: int

    class Config:
        from_attributes = True


class MealLogOut(BaseModel):
    id: int
    logged_date: date
    notes: str
    total_calories: float
    total_protein: float
    total_fat: float
    total_carbs: float
    photo_url: str | None
    items: list[MealLogItemOut]

    class Config:
        from_attributes = True


class MealPhotoResult(BaseModel):
    items: list[MealLogItemIn]
    total_calories: float
    total_protein: float
    total_fat: float
    total_carbs: float
    needs_clarification: bool = False
    question: str | None = None


class MealPhotoResponse(BaseModel):
    result: MealPhotoResult
    ai_raw: dict = Field(default_factory=dict)
