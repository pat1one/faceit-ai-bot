"""Unit tests for CaptchaService behavior."""

import pytest

import src.server.services.captcha_service as captcha_module
from src.server.services.captcha_service import (
    CaptchaService,
    CaptchaProviderError,
)


@pytest.mark.asyncio
async def test_verify_token_returns_true_when_disabled(monkeypatch):
    service = CaptchaService()
    monkeypatch.setattr(service, "is_enabled", lambda: False)

    ok = await service.verify_token(token=None)

    assert ok is True


@pytest.mark.asyncio
async def test_verify_token_missing_token_returns_false_when_enabled(monkeypatch):
    service = CaptchaService()
    monkeypatch.setattr(service, "is_enabled", lambda: True)

    ok = await service.verify_token(token=None)

    assert ok is False


@pytest.mark.asyncio
async def test_verify_token_delegates_to_turnstile_success(monkeypatch):
    service = CaptchaService()
    monkeypatch.setattr(service, "is_enabled", lambda: True)
    monkeypatch.setattr(service, "provider", "turnstile")

    async def fake_verify(token: str, remote_ip=None, action=None):  # noqa: ARG001
        assert token == "token123"
        return True

    monkeypatch.setattr(service, "_verify_turnstile", fake_verify)

    ok = await service.verify_token(token="token123")

    assert ok is True


@pytest.mark.asyncio
async def test_verify_token_provider_error_fail_open(monkeypatch):
    service = CaptchaService()
    monkeypatch.setattr(service, "is_enabled", lambda: True)
    monkeypatch.setattr(service, "provider", "turnstile")

    async def fake_verify(token: str, remote_ip=None, action=None):  # noqa: ARG001
        raise CaptchaProviderError("temporary error")

    monkeypatch.setattr(service, "_verify_turnstile", fake_verify)

    ok = await service.verify_token(token="token123", fail_open_on_error=True)

    assert ok is True


@pytest.mark.asyncio
async def test_verify_token_provider_error_fail_closed(monkeypatch):
    service = CaptchaService()
    monkeypatch.setattr(service, "is_enabled", lambda: True)
    monkeypatch.setattr(service, "provider", "turnstile")

    async def fake_verify(token: str, remote_ip=None, action=None):  # noqa: ARG001
        raise CaptchaProviderError("temporary error")

    monkeypatch.setattr(service, "_verify_turnstile", fake_verify)

    ok = await service.verify_token(token="token123", fail_open_on_error=False)

    assert ok is False


@pytest.mark.asyncio
async def test_verify_token_unknown_provider_fails_open(monkeypatch):
    service = CaptchaService()
    monkeypatch.setattr(service, "is_enabled", lambda: True)
    monkeypatch.setattr(service, "provider", "unknown_provider")

    ok = await service.verify_token(token="any")

    assert ok is True


def test_is_enabled_turnstile_with_and_without_secret():
    service = CaptchaService()

    service.provider = "turnstile"
    service.turnstile_secret_key = "secret-key"
    assert service.is_enabled() is True

    service.turnstile_secret_key = None
    assert service.is_enabled() is False


def test_is_enabled_smartcaptcha_with_and_without_secret():
    service = CaptchaService()

    for provider in ("smartcaptcha", "yandex_smartcaptcha", "yandex"):
        service.provider = provider
        service.smartcaptcha_secret_key = "secret-key"
        assert service.is_enabled() is True

        service.smartcaptcha_secret_key = None
        assert service.is_enabled() is False


def test_is_enabled_unknown_provider_returns_false():
    service = CaptchaService()
    service.provider = ""
    service.turnstile_secret_key = "secret-key"
    service.smartcaptcha_secret_key = "secret-key"

    assert service.is_enabled() is False


class _FakeResponse:
    """Minimal aiohttp response stub supporting async context manager."""

    def __init__(self, status: int, payload: dict | None = None, text: str = "") -> None:
        self.status = status
        self._payload = payload or {}
        self._text = text

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):  # noqa: D401, ANN001
        return False

    async def json(self) -> dict:
        return self._payload

    async def text(self) -> str:
        return self._text


class _FakeClientSession:
    """Minimal aiohttp.ClientSession stub for POST requests."""

    def __init__(self, *args, **kwargs) -> None:  # noqa: ANN001
        self.timeout = kwargs.get("timeout")
        self.last_url: str | None = None
        self.last_data: dict | None = None
        # Response instance is injected by tests via monkeypatching
        self._response: _FakeResponse | None = None

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):  # noqa: D401, ANN001
        return False

    def post(self, url: str, data: dict | None = None) -> _FakeResponse:
        self.last_url = url
        self.last_data = data or {}
        assert self._response is not None, "_response must be set in test"
        return self._response


@pytest.mark.asyncio
async def test_verify_turnstile_happy_path(monkeypatch):
    """_verify_turnstile should return True when provider responds with success."""

    service = CaptchaService()
    service.turnstile_secret_key = "secret-key"

    fake_resp = _FakeResponse(status=200, payload={"success": True})

    fake_session = _FakeClientSession()
    fake_session._response = fake_resp

    class _FakeAiohttp:
        class ClientTimeout:  # noqa: D401
            def __init__(self, total=None):  # noqa: ANN001
                self.total = total

        @staticmethod
        def ClientSession(timeout=None):  # noqa: ANN001
            return fake_session

    monkeypatch.setattr(captcha_module, "aiohttp", _FakeAiohttp)

    ok = await service._verify_turnstile("token123", remote_ip="1.2.3.4", action="login")

    assert ok is True
    assert fake_session.last_url.endswith("/turnstile/v0/siteverify")
    assert fake_session.last_data["secret"] == "secret-key"
    assert fake_session.last_data["response"] == "token123"
    assert fake_session.last_data["remoteip"] == "1.2.3.4"


@pytest.mark.asyncio
async def test_verify_turnstile_failure_logs_and_returns_false(monkeypatch, caplog):
    """_verify_turnstile should return False when provider reports failure."""

    service = CaptchaService()
    service.turnstile_secret_key = "secret-key"

    fake_resp = _FakeResponse(status=200, payload={"success": False, "error-codes": ["invalid-input-response"]})

    fake_session = _FakeClientSession()
    fake_session._response = fake_resp

    class _FakeAiohttp:
        ClientTimeout = captcha_module.aiohttp.ClientTimeout

        @staticmethod
        def ClientSession(timeout=None):  # noqa: ANN001
            return fake_session

    monkeypatch.setattr(captcha_module, "aiohttp", _FakeAiohttp)

    with caplog.at_level("INFO"):
        ok = await service._verify_turnstile("token123")

    assert ok is False
    assert any("Turnstile verification failed" in message for message in caplog.messages)


@pytest.mark.asyncio
async def test_verify_smartcaptcha_happy_path(monkeypatch):
    """_verify_smartcaptcha should return True when status is 'ok'."""

    service = CaptchaService()
    service.smartcaptcha_secret_key = "secret-key"

    fake_resp = _FakeResponse(status=200, payload={"status": "ok"})

    fake_session = _FakeClientSession()
    fake_session._response = fake_resp

    class _FakeAiohttp:
        ClientTimeout = captcha_module.aiohttp.ClientTimeout

        @staticmethod
        def ClientSession(timeout=None):  # noqa: ANN001
            return fake_session

    monkeypatch.setattr(captcha_module, "aiohttp", _FakeAiohttp)

    ok = await service._verify_smartcaptcha("token123", remote_ip="1.2.3.4")

    assert ok is True
    assert fake_session.last_url.endswith("/validate")
    assert fake_session.last_data["secret"] == "secret-key"
    assert fake_session.last_data["token"] == "token123"
    assert fake_session.last_data["ip"] == "1.2.3.4"


@pytest.mark.asyncio
async def test_verify_smartcaptcha_failure_returns_false(monkeypatch):
    """_verify_smartcaptcha should return False when status is not 'ok'."""

    service = CaptchaService()
    service.smartcaptcha_secret_key = "secret-key"

    fake_resp = _FakeResponse(status=200, payload={"status": "failed"})

    fake_session = _FakeClientSession()
    fake_session._response = fake_resp

    class _FakeAiohttp:
        ClientTimeout = captcha_module.aiohttp.ClientTimeout

        @staticmethod
        def ClientSession(timeout=None):  # noqa: ANN001
            return fake_session

    monkeypatch.setattr(captcha_module, "aiohttp", _FakeAiohttp)

    ok = await service._verify_smartcaptcha("token123")

    assert ok is False
