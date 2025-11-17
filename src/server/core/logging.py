"""Logging configuration with optional structlog integration.

В production-контейнере structlog может быть не установлен, поэтому
конфигурация должна уметь работать в двух режимах:

- с structlog (локальная разработка / полноценный образ с зависимостью);
- только с стандартным logging (fallback, если зависимость отсутствует).
"""

import logging
import logging.config
import sys
from typing import Any

try:
    import structlog
    from structlog.stdlib import LoggerFactory
    from structlog.processors import (
        TimeStamper,
        add_log_level,
        StackInfoRenderer,
        JSONRenderer,
        ConsoleRenderer,
    )

    STRUCTLOG_AVAILABLE = True
except ImportError:  # structlog не установлен в окружении
    structlog = None  # type: ignore[assignment]
    LoggerFactory = None  # type: ignore[assignment]
    TimeStamper = add_log_level = StackInfoRenderer = JSONRenderer = ConsoleRenderer = None
    STRUCTLOG_AVAILABLE = False

from ..config.settings import settings


def setup_logging() -> None:
    """Configure logging for the application.

    Если structlog доступен, настраивается структурированное логирование.
    Если нет — используется стандартный logging.basicConfig.
    """

    if STRUCTLOG_AVAILABLE and structlog is not None:  # type: ignore[truthy-function]
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

        # Configure standard logging to integrate with structlog
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
                        "console"
                        if settings.ENVIRONMENT != "production"
                        else "json"
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
    else:
        # Fallback: простой формат логов через стандартный logging
        logging.basicConfig(
            level=settings.LOG_LEVEL,
            format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            stream=sys.stdout,
        )


def get_logger(name: str) -> Any:
    """Get a logger instance.

    Возвращает structlog-логгер, если он доступен, иначе стандартный
    logging.Logger. Так код выше может работать одинаково в обоих режимах.
    """

    if STRUCTLOG_AVAILABLE and structlog is not None:
        return structlog.get_logger(name)  # type: ignore[no-any-return]

    return logging.getLogger(name)
