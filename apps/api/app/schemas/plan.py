from datetime import date

from pydantic import BaseModel


class MealItemOut(BaseModel):
    recipe_id: int
    servings: float

    class Config:
        from_attributes = True


class MealOut(BaseModel):
    id: int
    name: str
    calories: float
    protein: float
    fat: float
    carbs: float
    items: list[MealItemOut]

    class Config:
        from_attributes = True


class MealDayOut(BaseModel):
    id: int
    date: date
    total_calories: float
    total_protein: float
    total_fat: float
    total_carbs: float
    meals: list[MealOut]

    class Config:
        from_attributes = True


class MealPlanOut(BaseModel):
    id: int
    start_date: date
    end_date: date
    target_calories: float
    target_protein: float
    target_fat: float
    target_carbs: float
    days: list[MealDayOut]

    class Config:
        from_attributes = True
