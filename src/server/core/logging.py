"""Logging configuration with structlog integration."""

import logging
import logging.config
import sys

import structlog
from structlog.stdlib import LoggerFactory
from structlog.processors import (
    TimeStamper,
    add_log_level,
    StackInfoRenderer,
    JSONRenderer,
    ConsoleRenderer,
)

from ..config.settings import settings


def setup_logging() -> None:
    """Configure structured logging for the application."""

    # Configure structlog processors
    processors = [
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        add_log_level,
        structlog.stdlib.add_log_level,
        TimeStamper(fmt="iso"),
        StackInfoRenderer(),
    ]

    # Use JSON renderer in production, console in development
    if settings.ENVIRONMENT == "production":
        processors.append(JSONRenderer())
    else:
        processors.append(ConsoleRenderer(colors=True))

    structlog.configure(
        processors=processors,
        wrapper_class=structlog.stdlib.BoundLogger,
        logger_factory=LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    # Configure standard logging
    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "json": {
                "()": structlog.stdlib.ProcessorFormatter,
                "processor": structlog.processors.JSONRenderer(),
            },
            "console": {
                "()": structlog.stdlib.ProcessorFormatter,
                "processor": structlog.dev.ConsoleRenderer(colors=True),
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": (
                    "console" if settings.ENVIRONMENT != "production" else "json"
                ),
                "stream": sys.stdout,
            },
        },
        "loggers": {
            "": {
                "handlers": ["console"],
                "level": settings.LOG_LEVEL,
                "propagate": True,
            },
            "uvicorn": {
                "handlers": ["console"],
                "level": "INFO",
                "propagate": False,
            },
            "uvicorn.access": {
                "handlers": ["console"],
                "level": "INFO",
                "propagate": False,
            },
            "sqlalchemy.engine": {
                "handlers": ["console"],
                "level": "WARNING",
                "propagate": False,
            },
        },
    }

    logging.config.dictConfig(logging_config)


def get_logger(name: str) -> structlog.stdlib.BoundLogger:
    """Get a structured logger instance."""
    return structlog.get_logger(name)
