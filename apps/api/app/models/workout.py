from datetime import date

from sqlalchemy import Date, Float, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class WorkoutPlan(Base):
    __tablename__ = "workout_plans"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    start_date: Mapped[date] = mapped_column(Date)
    end_date: Mapped[date] = mapped_column(Date)
    template: Mapped[str] = mapped_column(String(50))

    days: Mapped[list["WorkoutDay"]] = relationship(
        "WorkoutDay", back_populates="plan", cascade="all, delete-orphan"
    )


class WorkoutDay(Base):
    __tablename__ = "workout_days"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    plan_id: Mapped[int] = mapped_column(ForeignKey("workout_plans.id"), index=True)
    date: Mapped[date] = mapped_column(Date)

    plan: Mapped[WorkoutPlan] = relationship("WorkoutPlan", back_populates="days")
    sessions: Mapped[list["WorkoutSession"]] = relationship(
        "WorkoutSession", back_populates="day", cascade="all, delete-orphan"
    )


class WorkoutSession(Base):
    __tablename__ = "workout_sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    day_id: Mapped[int] = mapped_column(ForeignKey("workout_days.id"), index=True)
    name: Mapped[str] = mapped_column(String(100))

    day: Mapped[WorkoutDay] = relationship("WorkoutDay", back_populates="sessions")
    exercises: Mapped[list["WorkoutExercise"]] = relationship(
        "WorkoutExercise", back_populates="session", cascade="all, delete-orphan"
    )


class Exercise(Base):
    __tablename__ = "exercises"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True)
    description: Mapped[str] = mapped_column(String(255))
    muscle_group: Mapped[str] = mapped_column(String(100))
    contraindications: Mapped[list[str]] = mapped_column(JSONB, default=list)


class WorkoutExercise(Base):
    __tablename__ = "workout_exercises"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("workout_sessions.id"), index=True)
    exercise_id: Mapped[int] = mapped_column(ForeignKey("exercises.id"), index=True)
    sets: Mapped[int] = mapped_column(Integer)
    reps: Mapped[int] = mapped_column(Integer)
    rest_seconds: Mapped[int] = mapped_column(Integer)
    rpe: Mapped[float] = mapped_column(Float)

    session: Mapped[WorkoutSession] = relationship("WorkoutSession", back_populates="exercises")
