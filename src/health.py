"""
Health check endpoints для мониторинга
"""

from fastapi import APIRouter
from datetime import datetime
import psutil
import os

router = APIRouter()


@router.get("/health")
async def health_check():
    """Базовая проверка работоспособности"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": os.getenv("VERSION", "0.3.0")
    }


@router.get("/health/detailed")
async def detailed_health():
    """Детальная проверка всех сервисов"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": os.getenv("VERSION", "0.3.0"),
        "system": {
            "cpu_percent": psutil.cpu_percent(),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_percent": psutil.disk_usage('/').percent
        },
        "services": {
            "database": await check_database(),
            "redis": await check_redis(),
            "api": "healthy"
        }
    }


async def check_database():
    """Проверка подключения к БД"""
    try:
        # TODO: проверка подключения к PostgreSQL
        return "healthy"
    except Exception:
        return "unhealthy"


async def check_redis():
    """Проверка подключения к Redis"""
    try:
        # TODO: проверка подключения к Redis
        return "healthy"
    except Exception:
        return "unhealthy"
