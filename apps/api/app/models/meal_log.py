from datetime import date, datetime

from sqlalchemy import Date, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class MealLog(Base):
    __tablename__ = "meal_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    logged_date: Mapped[date] = mapped_column(Date)
    notes: Mapped[str] = mapped_column(String(255), default="")
    total_calories: Mapped[float] = mapped_column(Float)
    total_protein: Mapped[float] = mapped_column(Float)
    total_fat: Mapped[float] = mapped_column(Float)
    total_carbs: Mapped[float] = mapped_column(Float)
    photo_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    ai_raw: Mapped[dict] = mapped_column(JSONB, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    items: Mapped[list["MealLogItem"]] = relationship(
        "MealLogItem", back_populates="meal_log", cascade="all, delete-orphan"
    )


class MealLogItem(Base):
    __tablename__ = "meal_log_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    meal_log_id: Mapped[int] = mapped_column(ForeignKey("meal_logs.id"), index=True)
    name: Mapped[str] = mapped_column(String(120))
    grams_estimate: Mapped[float] = mapped_column(Float)
    calories: Mapped[float] = mapped_column(Float)
    protein: Mapped[float] = mapped_column(Float)
    fat: Mapped[float] = mapped_column(Float)
    carbs: Mapped[float] = mapped_column(Float)
    confidence: Mapped[float] = mapped_column(Float)

    meal_log: Mapped[MealLog] = relationship("MealLog", back_populates="items")
