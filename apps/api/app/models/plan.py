from datetime import date

from sqlalchemy import Date, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class MealPlan(Base):
    __tablename__ = "meal_plans"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    start_date: Mapped[date] = mapped_column(Date)
    end_date: Mapped[date] = mapped_column(Date)
    target_calories: Mapped[float] = mapped_column(Float)
    target_protein: Mapped[float] = mapped_column(Float)
    target_fat: Mapped[float] = mapped_column(Float)
    target_carbs: Mapped[float] = mapped_column(Float)

    days: Mapped[list["MealDay"]] = relationship(
        "MealDay", back_populates="plan", cascade="all, delete-orphan"
    )


class MealDay(Base):
    __tablename__ = "meal_days"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    plan_id: Mapped[int] = mapped_column(ForeignKey("meal_plans.id"), index=True)
    date: Mapped[date] = mapped_column(Date)
    total_calories: Mapped[float] = mapped_column(Float)
    total_protein: Mapped[float] = mapped_column(Float)
    total_fat: Mapped[float] = mapped_column(Float)
    total_carbs: Mapped[float] = mapped_column(Float)

    plan: Mapped[MealPlan] = relationship("MealPlan", back_populates="days")
    meals: Mapped[list["Meal"]] = relationship(
        "Meal", back_populates="day", cascade="all, delete-orphan"
    )


class Meal(Base):
    __tablename__ = "meals"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    day_id: Mapped[int] = mapped_column(ForeignKey("meal_days.id"), index=True)
    name: Mapped[str] = mapped_column(String(120))
    calories: Mapped[float] = mapped_column(Float)
    protein: Mapped[float] = mapped_column(Float)
    fat: Mapped[float] = mapped_column(Float)
    carbs: Mapped[float] = mapped_column(Float)

    day: Mapped[MealDay] = relationship("MealDay", back_populates="meals")
    items: Mapped[list["MealItem"]] = relationship(
        "MealItem", back_populates="meal", cascade="all, delete-orphan"
    )


class MealItem(Base):
    __tablename__ = "meal_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    meal_id: Mapped[int] = mapped_column(ForeignKey("meals.id"), index=True)
    recipe_id: Mapped[int] = mapped_column(ForeignKey("recipes.id"), index=True)
    servings: Mapped[float] = mapped_column(Float, default=1.0)

    meal: Mapped[Meal] = relationship("Meal", back_populates="items")
