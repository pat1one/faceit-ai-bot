"""Unit tests for middleware.rate_limiter.RateLimiter.

Covers both in-memory fallback and Redis-backed paths,
including limit exceed and bypass user logic.
"""

import pytest
from fastapi import HTTPException
from starlette.requests import Request

from src.server.config.settings import settings
import src.server.middleware.rate_limiter as rl_mod
from src.server.middleware.rate_limiter import RateLimiter


class DummyRedis:
    """Minimal async Redis stub for RateLimiter tests."""

    def __init__(self) -> None:
        self.counters: dict[str, int] = {}
        self.expires: dict[str, int] = {}

    async def incr(self, key: str) -> int:
        self.counters[key] = self.counters.get(key, 0) + 1
        return self.counters[key]

    async def expire(self, key: str, ttl: int) -> None:
        self.expires[key] = ttl


def make_request(path: str = "/test", headers: dict[str, str] | None = None) -> Request:
    if headers is None:
        raw_headers = []
    else:
        raw_headers = [(k.lower().encode("latin-1"), v.encode("latin-1")) for k, v in headers.items()]

    scope = {
        "type": "http",
        "method": "GET",
        "path": path,
        "headers": raw_headers,
        "client": ("127.0.0.1", 50000),
    }
    return Request(scope)


@pytest.mark.asyncio
async def test_rate_limiter_fallback_memory_exceeds_minute_limit():
    """Without Redis client, RateLimiter should use in-memory counters and return 429 when limit exceeded."""
    limiter = RateLimiter(requests_per_minute=2, requests_per_hour=1000)
    limiter.redis_client = None  # force fallback

    request = make_request()

    await limiter(request)
    await limiter(request)

    with pytest.raises(HTTPException) as exc:
        await limiter(request)

    assert exc.value.status_code == 429
    assert "2 requests per minute" in exc.value.detail


@pytest.mark.asyncio
async def test_rate_limiter_redis_path_exceeds_minute_limit(monkeypatch):
    """With Redis client set, exceeding per-minute limit should produce 429 via Redis-backed counters."""
    limiter = RateLimiter(requests_per_minute=1, requests_per_hour=1000)

    dummy = DummyRedis()
    limiter.redis_client = dummy

    monkeypatch.setattr(settings, "RATE_LIMIT_BAN_ENABLED", False, raising=False)
    monkeypatch.setattr(settings, "RATE_LIMIT_BYPASS_USER_ID", None, raising=False)

    def fake_decode(token: str):  # noqa: ARG001
        return {"sub": "123"}

    monkeypatch.setattr(rl_mod, "decode_access_token", fake_decode)

    request = make_request(headers={"Authorization": "Bearer sometoken"})

    await limiter(request)

    with pytest.raises(HTTPException) as exc:
        await limiter(request)

    assert exc.value.status_code == 429
    assert "1 requests per minute" in exc.value.detail


@pytest.mark.asyncio
async def test_rate_limiter_bypass_user_id_skips_limits(monkeypatch):
    """If RATE_LIMIT_BYPASS_USER_ID matches token sub, limits are not applied and Redis is not used."""
    limiter = RateLimiter(requests_per_minute=1, requests_per_hour=1)

    dummy = DummyRedis()
    limiter.redis_client = dummy

    monkeypatch.setattr(settings, "RATE_LIMIT_BAN_ENABLED", False, raising=False)
    monkeypatch.setattr(settings, "RATE_LIMIT_BYPASS_USER_ID", "42", raising=False)

    def fake_decode(token: str):  # noqa: ARG001
        return {"sub": "42"}

    monkeypatch.setattr(rl_mod, "decode_access_token", fake_decode)

    request = make_request(headers={"Authorization": "Bearer bypass"})

    allowed, message = await limiter.check_rate_limit(request)

    assert allowed is True
    assert message == "OK"
    assert dummy.counters == {}
