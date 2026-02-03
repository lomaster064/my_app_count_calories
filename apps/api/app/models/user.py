from datetime import date, datetime
from typing import Optional

from sqlalchemy import Date, DateTime, Enum, Float, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    name: Mapped[str] = mapped_column(String(120))
    gender: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    birth_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    height_cm: Mapped[float] = mapped_column(Float)
    current_weight_kg: Mapped[float] = mapped_column(Float)
    target_weight_kg: Mapped[float] = mapped_column(Float)
    goal: Mapped[str] = mapped_column(Enum("cut", "bulk", name="goal_enum"))
    activity_level: Mapped[str] = mapped_column(Enum("low", "medium", "high", name="activity_enum"))
    training_level: Mapped[str] = mapped_column(
        Enum("beginner", "intermediate", "advanced", name="training_enum")
    )

    allergies: Mapped[list[str]] = mapped_column(JSONB, default=list)
    intolerances: Mapped[list[str]] = mapped_column(JSONB, default=list)
    diet_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    dislikes: Mapped[list[str]] = mapped_column(JSONB, default=list)

    meals_per_day: Mapped[int] = mapped_column(Integer, default=3)
    meal_time_preferences: Mapped[list[str]] = mapped_column(JSONB, default=list)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    injuries: Mapped[list["Injury"]] = relationship("Injury", back_populates="user")


class Injury(Base):
    __tablename__ = "injuries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    injury_type: Mapped[str] = mapped_column(String(120))
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    restricted_exercises: Mapped[list[str]] = mapped_column(JSONB, default=list)

    user: Mapped[User] = relationship("User", back_populates="injuries")
