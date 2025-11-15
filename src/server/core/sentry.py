"""Sentry integration for error tracking and monitoring."""

import logging
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
from sentry_sdk.integrations.redis import RedisIntegration
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.logging import LoggingIntegration

from ..config.settings import Settings

logger = logging.getLogger(__name__)


class SentryManager:
    """Manages Sentry integration for error tracking."""
    
    def __init__(self):
        self.settings = Settings()
        self.enabled = bool(self.settings.SENTRY_DSN)
        
    def init_sentry(self):
        """Initialize Sentry SDK with appropriate integrations."""
        if not self.enabled:
            logger.info("Sentry is disabled - no DSN provided")
            return
            
        try:
            # Configure logging integration
            logging_integration = LoggingIntegration(
                level=logging.INFO,
                event_level=logging.ERROR
            )
            
            # Initialize Sentry with integrations
            sentry_sdk.init(
                dsn=self.settings.SENTRY_DSN,
                integrations=[
                    FastApiIntegration(auto_enabling_integrations=False),
                    SqlalchemyIntegration(),
                    RedisIntegration(),
                    CeleryIntegration(),
                    logging_integration,
                ],
                traces_sample_rate=0.1,  # 10% of transactions for performance monitoring
                environment=self.settings.ENVIRONMENT,
                release=self.settings.VERSION,
                send_default_pii=False,  # Don't send personally identifiable information
            )
            
            logger.info("Sentry initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Sentry: {str(e)}")
            
    def capture_exception(self, exception, context=None):
        """Capture exception with additional context."""
        if not self.enabled:
            return
            
        try:
            with sentry_sdk.configure_scope() as scope:
                if context:
                    for key, value in context.items():
                        scope.set_extra(key, value)
                        
                sentry_sdk.capture_exception(exception)
                
        except Exception as e:
            logger.error(f"Failed to capture exception in Sentry: {str(e)}")
            
    def capture_message(self, message, level="info"):
        """Capture a message with specified severity level."""
        if not self.enabled:
            return
            
        try:
            sentry_sdk.capture_message(message, level=level)
        except Exception as e:
            logger.error(f"Failed to capture message in Sentry: {str(e)}")
            
    def set_user_context(self, user_id=None, email=None, username=None):
        """Set user context for Sentry events."""
        if not self.enabled:
            return
            
        try:
            with sentry_sdk.configure_scope() as scope:
                user_data = {}
                if user_id:
                    user_data["id"] = user_id
                if email:
                    user_data["email"] = email
                if username:
                    user_data["username"] = username
                    
                if user_data:
                    scope.set_user(user_data)
                    
        except Exception as e:
            logger.error(f"Failed to set user context in Sentry: {str(e)}")
            
    def set_tag(self, key, value):
        """Set a tag for Sentry events."""
        if not self.enabled:
            return
            
        try:
            sentry_sdk.set_tag(key, value)
        except Exception as e:
            logger.error(f"Failed to set tag in Sentry: {str(e)}")
            
    def add_breadcrumb(self, message, category="custom", level="info"):
        """Add a breadcrumb to Sentry events."""
        if not self.enabled:
            return
            
        try:
            sentry_sdk.add_breadcrumb(
                message=message,
                category=category,
                level=level
            )
        except Exception as e:
            logger.error(f"Failed to add breadcrumb in Sentry: {str(e)}")


# Global Sentry manager instance
sentry_manager = SentryManager()


def init_sentry():
    """Initialize Sentry for the application."""
    sentry_manager.init_sentry()


def capture_exception(exception, context=None):
    """Capture exception with context."""
    sentry_manager.capture_exception(exception, context)


def capture_message(message, level="info"):
    """Capture a message."""
    sentry_manager.capture_message(message, level)


def set_user_context(user_id=None, email=None, username=None):
    """Set user context."""
    sentry_manager.set_user_context(user_id, email, username)


def set_tag(key, value):
    """Set a tag."""
    sentry_manager.set_tag(key, value)


def add_breadcrumb(message, category="custom", level="info"):
    """Add a breadcrumb."""
    sentry_manager.add_breadcrumb(message, category, level)
