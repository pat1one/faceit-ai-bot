"""
Rate limiting middleware
"""

from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
import redis
import os
from datetime import datetime, timedelta

redis_client = redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379"))


class RateLimiter:
    """Rate limiter на базе Redis"""
    
    def __init__(self, requests: int = 100, window: int = 3600):
        self.requests = requests
        self.window = window
    
    async def check_rate_limit(self, request: Request):
        """Проверить rate limit для IP"""
        
        # Получить IP клиента
        client_ip = request.client.host
        key = f"rate_limit:{client_ip}"
        
        # Проверить текущее количество запросов
        current = redis_client.get(key)
        
        if current is None:
            # Первый запрос
            redis_client.setex(key, self.window, 1)
            return True
        
        current = int(current)
        
        if current >= self.requests:
            raise HTTPException(
                status_code=429,
                detail=f"Превышен лимит запросов. Максимум {self.requests} запросов в час."
            )
        
        # Увеличить счетчик
        redis_client.incr(key)
        return True


# Middleware для FastAPI
async def rate_limit_middleware(request: Request, call_next):
    """Middleware для проверки rate limit"""
    
    # Пропустить для некоторых путей
    if request.url.path in ["/health", "/metrics", "/docs"]:
        return await call_next(request)
    
    limiter = RateLimiter(requests=100, window=3600)
    await limiter.check_rate_limit(request)
    
    response = await call_next(request)
    return response
