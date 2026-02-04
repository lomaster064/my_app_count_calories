from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.meal_log import MealLog
from app.models.plan import MealDay, MealPlan
from app.models.user import User
from app.models.water import WaterLog
from app.utils.rebalance import rebalance_day

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/summary")
def dashboard_summary(
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

    consumed = (
        db.query(
            func.coalesce(func.sum(MealLog.total_calories), 0),
            func.coalesce(func.sum(MealLog.total_protein), 0),
            func.coalesce(func.sum(MealLog.total_fat), 0),
            func.coalesce(func.sum(MealLog.total_carbs), 0),
        )
        .filter(MealLog.user_id == current_user.id, MealLog.logged_date == day)
        .first()
    )

    water_total = (
        db.query(func.coalesce(func.sum(WaterLog.amount_ml), 0))
        .filter(WaterLog.user_id == current_user.id, WaterLog.logged_date == day)
        .scalar()
    )

    remaining_meals = max(len(plan_day.meals), 1)
    suggestion = rebalance_day(
        plan_day.total_calories,
        float(consumed[0]),
        remaining_meals,
        has_workout_today=True,
        injury_constraints=[injury.injury_type for injury in current_user.injuries],
    )

    return {
        "date": day,
        "target": {
            "calories": plan_day.total_calories,
            "protein": plan_day.total_protein,
            "fat": plan_day.total_fat,
            "carbs": plan_day.total_carbs,
        },
        "consumed": {
            "calories": float(consumed[0]),
            "protein": float(consumed[1]),
            "fat": float(consumed[2]),
            "carbs": float(consumed[3]),
        },
        "water_ml": int(water_total or 0),
        "rebalance": suggestion.__dict__,
    }
