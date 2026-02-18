from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.meal_log import MealLog
from app.models.plan import MealDay, MealPlan
from app.models.workout import WorkoutDay, WorkoutPlan
from app.models.user import User
from app.schemas.workout import WorkoutDayOut, WorkoutPlanOut
from app.utils.rebalance import rebalance_day
from app.services.workout_generator import generate_workout_plan

router = APIRouter(prefix="/workouts", tags=["workouts"])


@router.post("/generate", response_model=WorkoutPlanOut)
def generate_workout(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return generate_workout_plan(db, current_user)


@router.get("", response_model=WorkoutPlanOut)
def get_workout_plan(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    plan = (
        db.query(WorkoutPlan)
        .filter(WorkoutPlan.user_id == current_user.id)
        .order_by(WorkoutPlan.id.desc())
        .first()
    )
    if not plan:
        raise HTTPException(status_code=404, detail="Workout plan not found")
    return plan


@router.get("/day", response_model=WorkoutDayOut)
def get_workout_day(
    day: date, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    workout_day = (
        db.query(WorkoutDay)
        .join(WorkoutPlan, WorkoutDay.plan_id == WorkoutPlan.id)
        .filter(WorkoutPlan.user_id == current_user.id, WorkoutDay.date == day)
        .first()
    )
    if not workout_day:
        raise HTTPException(status_code=404, detail="Workout day not found")
    plan_day = (
        db.query(MealDay)
        .join(MealPlan, MealDay.plan_id == MealPlan.id)
        .filter(MealPlan.user_id == current_user.id, MealDay.date == day)
        .first()
    )
    consumed_calories = (
        db.query(MealLog.total_calories)
        .filter(MealLog.user_id == current_user.id, MealLog.logged_date == day)
        .all()
    )
    total_consumed = sum(item.total_calories for item in consumed_calories)
    adjustment = None
    if plan_day:
        suggestion = rebalance_day(
            plan_day.total_calories,
            total_consumed,
            remaining_meals=max(len(plan_day.meals), 1),
            has_workout_today=bool(workout_day.sessions),
            injury_constraints=[injury.injury_type for injury in current_user.injuries],
        )
        adjustment = suggestion.workout_suggestion

    response = WorkoutDayOut.model_validate(workout_day).model_dump()
    response["adjustment"] = adjustment
    return response
