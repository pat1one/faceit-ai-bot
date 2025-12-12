"""Background tasks"""
import logging
import asyncio
import os
from typing import Dict, Any

from celery import Task
from fastapi import UploadFile

from .celery_app import celery_app
from .features.demo_analyzer.service import DemoAnalyzer

logger = logging.getLogger(__name__)


class CallbackTask(Task):
    """Base task with callbacks"""

    def on_success(self, retval, task_id, args, kwargs):
        """Success callback"""
        logger.info(f"Task {task_id} completed successfully")

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        """Failure callback"""
        logger.error(f"Task {task_id} failed: {exc}")


@celery_app.task(
    bind=True,
    base=CallbackTask,
    max_retries=3,
    default_retry_delay=60,
)
def analyze_demo_task(
    self,
    demo_file_path: str,
    user_id: str | None = None,
    language: str = "ru",
) -> Dict:
    """Analyze demo file in background.

    Args:
        demo_file_path: Path to demo file
        user_id: Optional user ID (for logging/trace)
        language: Target language for analysis ("ru" or "en")

    Returns:
        JSON-serializable dict with analysis results
    """
    try:
        logger.info(
            "Demo analysis task started: path=%s, user_id=%s, language=%s",
            demo_file_path,
            user_id,
            language,
        )

        if not os.path.exists(demo_file_path):
            logger.error("Demo file not found: %s", demo_file_path)
            return {
                "status": "failed",
                "error": "Demo file not found",
                "user_id": user_id,
                "demo_path": demo_file_path,
            }

        analyzer = DemoAnalyzer()

        with open(demo_file_path, "rb") as file_obj:
            upload = UploadFile(
                filename=os.path.basename(demo_file_path),
                file=file_obj,
            )

            demo_analysis = asyncio.run(
                analyzer.analyze_demo(demo_file=upload, language=language)
            )

        result = {
            "status": "completed",
            "user_id": user_id,
            "demo_path": demo_file_path,
            "analysis": demo_analysis.model_dump(mode="json"),
        }

        logger.info(
            "Demo analysis completed for user %s, path=%s",
            user_id,
            demo_file_path,
        )
        return result

    except Exception as exc:
        logger.exception("Demo analysis failed: %s", exc)
        raise self.retry(exc=exc)
    finally:
        try:
            if os.path.exists(demo_file_path):
                os.unlink(demo_file_path)
        except Exception:
            # Best-effort cleanup, do not mask original errors
            pass


@celery_app.task(
    bind=True,
    base=CallbackTask,
    max_retries=5,
    default_retry_delay=300
)
def send_email_task(
    self,
    to_email: str,
    subject: str,
    body: str,
    template: str = None
) -> Dict:
    """
    Send email notification

    Args:
        to_email: Recipient email
        subject: Email subject
        body: Email body
        template: Template name

    Returns:
        Send status
    """
    try:
        logger.info(f"Sending email to {to_email}")

        # Email sending logic here
        # Use SMTP or email service (SendGrid, Mailgun, etc.)

        return {
            "status": "sent",
            "to": to_email,
            "subject": subject
        }

    except Exception as exc:
        logger.exception(f"Email sending failed: {exc}")
        raise self.retry(exc=exc)


@celery_app.task(
    bind=True,
    base=CallbackTask,
    max_retries=10,
    default_retry_delay=60
)
def process_webhook_task(
    self,
    provider: str,
    payload: Dict[str, Any]
) -> Dict:
    """
    Process payment webhook with retry

    Args:
        provider: Payment provider name
        payload: Webhook payload

    Returns:
        Processing result
    """
    try:
        logger.info(f"Processing {provider} webhook")

        # Process webhook logic here

        logger.info(f"Webhook processed successfully: {provider}")
        return {
            "status": "processed",
            "provider": provider
        }

    except Exception as exc:
        logger.exception(f"Webhook processing failed: {exc}")
        raise self.retry(exc=exc)


@celery_app.task(bind=True, base=CallbackTask)
def analyze_player_task(self, player_nickname: str) -> Dict:
    """
    Analyze player in background

    Args:
        player_nickname: Player nickname

    Returns:
        Analysis results
    """
    try:
        logger.info(f"Player analysis started: {player_nickname}")

        # Analysis logic here

        return {
            "status": "completed",
            "player": player_nickname
        }

    except Exception as exc:
        logger.exception(f"Player analysis failed: {exc}")
        raise self.retry(exc=exc)


@celery_app.task(bind=True)
def cleanup_old_data_task(self, days: int = 30) -> Dict:
    """
    Cleanup old data (daily task)

    Args:
        days: Delete data older than N days

    Returns:
        Cleanup stats
    """
    try:
        logger.info(f"Cleanup started: older than {days} days")

        # Cleanup logic:
        # - Old demo files
        # - Expired cache
        # - Old logs

        return {
            "status": "completed",
            "deleted_records": 0
        }

    except Exception as exc:
        logger.exception(f"Cleanup failed: {exc}")
        return {"status": "failed", "error": str(exc)}


@celery_app.task
def check_subscription_expiry_task() -> Dict:
    """
    Check and notify users about subscription expiry

    Returns:
        Notification stats
    """
    try:
        logger.info("Checking subscription expiry")

        # Logic:
        # 1. Find subscriptions expiring in 3 days
        # 2. Send email notifications
        # 3. Deactivate expired subscriptions

        return {
            "status": "completed",
            "notified_users": 0,
            "deactivated": 0
        }

    except Exception as exc:
        logger.exception(f"Subscription check failed: {exc}")
        return {"status": "failed", "error": str(exc)}


@celery_app.task
def send_weekly_reports_task() -> Dict:
    """
    Send weekly performance reports to users

    Returns:
        Report stats
    """
    try:
        logger.info("Sending weekly reports")

        # Logic:
        # 1. Get active premium users
        # 2. Generate performance reports
        # 3. Send emails

        return {
            "status": "completed",
            "reports_sent": 0
        }

    except Exception as exc:
        logger.exception(f"Weekly reports failed: {exc}")
        return {"status": "failed", "error": str(exc)}
