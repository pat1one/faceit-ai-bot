"""Celery configuration"""
from celery import Celery
import os

# Redis connection
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# Celery app
celery_app = Celery(
    "faceit_bot",
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=["src.server.tasks"]
)

# Configuration
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
    task_soft_time_limit=25 * 60,  # 25 minutes
    worker_prefetch_multiplier=4,
    worker_max_tasks_per_child=1000,
    task_acks_late=True,
    task_reject_on_worker_lost=True,
)

# Task routes
celery_app.conf.task_routes = {
    "src.server.tasks.analyze_demo_task": {"queue": "demo_analysis"},
    "src.server.tasks.send_email_task": {"queue": "notifications"},
    "src.server.tasks.process_webhook_task": {"queue": "webhooks"},
}
