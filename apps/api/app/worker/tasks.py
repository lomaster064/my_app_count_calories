from app.db.session import SessionLocal
from app.models.user import User
from app.services.plan_generator import generate_meal_plan
from app.services.workout_generator import generate_workout_plan
from app.worker.celery_app import celery_app


@celery_app.task
def generate_plans(user_id: int) -> dict:
    db = SessionLocal()
    try:
        user = db.get(User, user_id)
        if not user:
            return {"status": "not_found"}
        meal_plan = generate_meal_plan(db, user)
        workout_plan = generate_workout_plan(db, user)
        return {"status": "ok", "meal_plan_id": meal_plan["plan"].id, "workout_plan_id": workout_plan.id}
    finally:
        db.close()
