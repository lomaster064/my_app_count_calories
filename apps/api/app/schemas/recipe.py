from pydantic import BaseModel


class RecipeIngredientOut(BaseModel):
    name: str
    grams: float

    class Config:
        from_attributes = True


class RecipeOut(BaseModel):
    id: int
    name: str
    description: str
    instructions: list[str]
    tags: list[str]
    calories: float
    protein: float
    fat: float
    carbs: float
    ingredients: list[RecipeIngredientOut]

    class Config:
        from_attributes = True
