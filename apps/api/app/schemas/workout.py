from datetime import date

from pydantic import BaseModel


class WorkoutExerciseOut(BaseModel):
    exercise_id: int
    sets: int
    reps: int
    rest_seconds: int
    rpe: float

    class Config:
        from_attributes = True


class WorkoutSessionOut(BaseModel):
    id: int
    name: str
    exercises: list[WorkoutExerciseOut]

    class Config:
        from_attributes = True


class WorkoutDayOut(BaseModel):
    id: int
    date: date
    sessions: list[WorkoutSessionOut]
    adjustment: str | None = None

    class Config:
        from_attributes = True


class WorkoutPlanOut(BaseModel):
    id: int
    start_date: date
    end_date: date
    template: str
    days: list[WorkoutDayOut]

    class Config:
        from_attributes = True
