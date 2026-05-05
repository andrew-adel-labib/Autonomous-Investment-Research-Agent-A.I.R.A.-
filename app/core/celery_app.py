from celery import Celery
from celery.schedules import crontab
from app.core.config import settings

celery = Celery(
    "AIRA",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=[
        "app.workers.tasks",
        "app.workers.scheduler"
    ]
)

celery.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,

    task_acks_late=True,
    worker_prefetch_multiplier=1,
    broker_connection_retry_on_startup=True,
)

celery.conf.beat_schedule = {
    "daily-analysis": {
        "task": "app.workers.scheduler.daily_analysis",
        "schedule": crontab(hour=9, minute=0),
    }
}

celery.autodiscover_tasks(["app.workers"])