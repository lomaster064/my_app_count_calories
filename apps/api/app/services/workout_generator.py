from datetime import date, timedelta

from sqlalchemy.orm import Session

from app.models.workout import Exercise, WorkoutDay, WorkoutExercise, WorkoutPlan, WorkoutSession
from app.models.user import User


WORKOUT_TEMPLATES = {
    "beginner": ["Full Body", "Rest", "Full Body", "Rest", "Full Body", "Rest", "Rest"],
    "intermediate": ["Upper", "Lower", "Rest", "Upper", "Lower", "Rest", "Rest"],
    "advanced": ["Push", "Pull", "Legs", "Rest", "Upper", "Lower", "Rest"],
}


def generate_workout_plan(db: Session, user: User) -> WorkoutPlan:
    today = date.today()
    end = today + timedelta(days=29)
    template = WORKOUT_TEMPLATES.get(user.training_level, WORKOUT_TEMPLATES["beginner"])

    plan = WorkoutPlan(user_id=user.id, start_date=today, end_date=end, template=user.training_level)
    exercises = db.query(Exercise).all()

    injury_constraints = {injury.injury_type for injury in user.injuries}

    for offset in range(30):
        day_date = today + timedelta(days=offset)
        day = WorkoutDay(date=day_date)
        session_name = template[offset % len(template)]
        if session_name != "Rest":
            session = WorkoutSession(name=session_name)
            for exercise in exercises[:4]:
                if any(constraint in exercise.contraindications for constraint in injury_constraints):
                    continue
                session.exercises.append(
                    WorkoutExercise(
                        exercise_id=exercise.id,
                        sets=3,
                        reps=10,
                        rest_seconds=90,
                        rpe=7.0,
                    )
                )
            day.sessions.append(session)
        plan.days.append(day)

    db.add(plan)
    db.commit()
    db.refresh(plan)
    return plan
