from datetime import date

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.meal_log import MealLog, MealLogItem
from app.models.plan import MealDay, MealPlan
from app.models.user import User
from app.schemas.meal_log import MealLogIn, MealLogOut, MealPhotoResponse, MealPhotoResult
from app.services.ai import analyze_food_photo
from app.services.storage import upload_bytes
from app.utils.rebalance import rebalance_day

router = APIRouter(prefix="/meal-logs", tags=["meal-logs"])


@router.post("", response_model=MealLogOut)
def create_meal_log(
    payload: MealLogIn, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    totals = {
        "calories": sum(item.calories for item in payload.items),
        "protein": sum(item.protein for item in payload.items),
        "fat": sum(item.fat for item in payload.items),
        "carbs": sum(item.carbs for item in payload.items),
    }
    log = MealLog(
        user_id=current_user.id,
        logged_date=payload.logged_date,
        notes=payload.notes,
        total_calories=totals["calories"],
        total_protein=totals["protein"],
        total_fat=totals["fat"],
        total_carbs=totals["carbs"],
    )
    for item in payload.items:
        log.items.append(MealLogItem(**item.model_dump()))
    db.add(log)
    db.commit()
    db.refresh(log)
    return log


@router.get("", response_model=list[MealLogOut])
def list_meal_logs(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(MealLog).filter(MealLog.user_id == current_user.id).all()


@router.post("/photo", response_model=MealPhotoResponse)
def log_meal_photo(
    logged_date: date,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    content = file.file.read()
    photo_url = upload_bytes(content, file.filename, file.content_type or "image/jpeg")
    ai_result, ai_raw = analyze_food_photo(photo_url)

    result = MealPhotoResult(
        items=[item.__dict__ for item in ai_result.items],
        total_calories=ai_result.total_calories,
        total_protein=ai_result.total_protein,
        total_fat=ai_result.total_fat,
        total_carbs=ai_result.total_carbs,
        needs_clarification=ai_result.needs_clarification,
        question=ai_result.question,
    )

    if not ai_result.needs_clarification:
        log = MealLog(
            user_id=current_user.id,
            logged_date=logged_date,
            notes="photo",
            total_calories=ai_result.total_calories,
            total_protein=ai_result.total_protein,
            total_fat=ai_result.total_fat,
            total_carbs=ai_result.total_carbs,
            photo_url=photo_url,
            ai_raw=ai_raw,
        )
        for item in ai_result.items:
            log.items.append(MealLogItem(**item.__dict__))
        db.add(log)
        db.commit()

    _ = _rebalance_if_needed(db, current_user, logged_date, ai_result.total_calories)

    return MealPhotoResponse(result=result, ai_raw=ai_raw)


def _rebalance_if_needed(db: Session, current_user: User, logged_date: date, consumed_calories: float):
    plan_day = (
        db.query(MealDay)
        .join(MealPlan, MealDay.plan_id == MealPlan.id)
        .filter(MealPlan.user_id == current_user.id, MealDay.date == logged_date)
        .first()
    )
    if not plan_day:
        return None
    remaining_meals = len(plan_day.meals)
    has_workout_today = True
    injury_constraints = [injury.injury_type for injury in current_user.injuries]
    return rebalance_day(
        plan_day.total_calories,
        consumed_calories,
        remaining_meals,
        has_workout_today,
        injury_constraints,
    )
