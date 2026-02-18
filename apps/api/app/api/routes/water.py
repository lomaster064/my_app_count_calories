from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.user import User
from app.models.water import WaterLog
from app.schemas.water import WaterLogIn, WaterLogOut

router = APIRouter(prefix="/water", tags=["water"])


@router.post("/log", response_model=WaterLogOut)
def log_water(
    payload: WaterLogIn, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    log = WaterLog(
        user_id=current_user.id,
        logged_date=payload.logged_date,
        amount_ml=payload.amount_ml,
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log


@router.get("/summary")
def water_summary(
    day: date, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    total = (
        db.query(WaterLog)
        .filter(WaterLog.user_id == current_user.id, WaterLog.logged_date == day)
        .with_entities(WaterLog.amount_ml)
        .all()
    )
    return {"date": day, "total_ml": sum(item.amount_ml for item in total)}
