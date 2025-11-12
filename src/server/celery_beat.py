"""Celery Beat periodic tasks configuration"""
from celery.schedules import crontab
from .celery_app import celery_app


celery_app.conf.beat_schedule = {
    "cleanup-old-data-daily": {
        "task": "src.server.tasks.cleanup_old_data_task",
        "schedule": crontab(hour=3, minute=0),  # 3:00 AM daily
        "args": (30,),  # Delete data older than 30 days
    },
    "check-subscription-expiry": {
        "task": "src.server.tasks.check_subscription_expiry_task",
        "schedule": crontab(hour=9, minute=0),  # 9:00 AM daily
    },
    "send-weekly-reports": {
        "task": "src.server.tasks.send_weekly_reports_task",
        "schedule": crontab(
            hour=10,
            minute=0,
            day_of_week=1
        ),  # Monday 10:00 AM
    },
}
