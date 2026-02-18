from celery import Celery

from app.core.config import settings

celery_app = Celery(
    "fitfuel",
    broker=settings.redis_url,
    backend=settings.redis_url,
)

celery_app.conf.task_routes = {
    "app.worker.tasks.generate_plans": {"queue": "default"},
}
