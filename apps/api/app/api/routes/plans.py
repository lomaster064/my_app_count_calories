from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.plan import MealDay, MealPlan
from app.models.user import User
from app.schemas.plan import MealDayOut, MealPlanOut
from app.services.plan_generator import generate_meal_plan

router = APIRouter(prefix="/plans", tags=["plans"])


@router.post("/generate")
def generate_plan(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = generate_meal_plan(db, current_user)
    return result


@router.get("", response_model=MealPlanOut)
def get_plan(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    plan = (
        db.query(MealPlan)
        .filter(MealPlan.user_id == current_user.id)
        .order_by(MealPlan.id.desc())
        .first()
    )
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    return plan


@router.get("/day", response_model=MealDayOut)
def get_plan_day(
    day: date, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    plan_day = (
        db.query(MealDay)
        .join(MealPlan, MealDay.plan_id == MealPlan.id)
        .filter(MealPlan.user_id == current_user.id, MealDay.date == day)
        .first()
    )
    if not plan_day:
        raise HTTPException(status_code=404, detail="Plan day not found")
    return plan_day
