from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.core.security import create_access_token, create_refresh_token, hash_password, verify_password
from app.models.user import Injury, User
from app.schemas.auth import LoginRequest, TokenPair
from app.schemas.user import UserCreate, UserOut

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserOut)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        email=payload.email,
        password_hash=hash_password(payload.password),
        name=payload.name,
        gender=payload.gender,
        birth_date=payload.birth_date,
        height_cm=payload.height_cm,
        current_weight_kg=payload.current_weight_kg,
        target_weight_kg=payload.target_weight_kg,
        goal=payload.goal,
        activity_level=payload.activity_level,
        training_level=payload.training_level,
        allergies=payload.allergies,
        intolerances=payload.intolerances,
        diet_type=payload.diet_type,
        dislikes=payload.dislikes,
        meals_per_day=payload.meals_per_day,
        meal_time_preferences=payload.meal_time_preferences,
    )
    db.add(user)
    db.flush()

    for injury_payload in payload.injuries:
        db.add(
            Injury(
                user_id=user.id,
                injury_type=injury_payload.injury_type,
                description=injury_payload.description,
                restricted_exercises=injury_payload.restricted_exercises,
            )
        )

    db.commit()
    db.refresh(user)
    return user


@router.post("/login", response_model=TokenPair)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    return TokenPair(
        access_token=create_access_token(str(user.id)),
        refresh_token=create_refresh_token(str(user.id)),
    )


@router.post("/refresh", response_model=TokenPair)
def refresh(current_user: User = Depends(get_current_user)):
    return TokenPair(
        access_token=create_access_token(str(current_user.id)),
        refresh_token=create_refresh_token(str(current_user.id)),
    )


@router.get("/me", response_model=UserOut)
def me(current_user: User = Depends(get_current_user)):
    return current_user
