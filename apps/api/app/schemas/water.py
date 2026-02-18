from datetime import date

from pydantic import BaseModel


class WaterLogIn(BaseModel):
    logged_date: date
    amount_ml: int


class WaterLogOut(BaseModel):
    id: int
    logged_date: date
    amount_ml: int

    class Config:
        from_attributes = True
