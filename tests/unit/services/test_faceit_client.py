"""Unit tests for Faceit client

Эти тесты относятся к старой синхронной реализации FaceitClient и временно
отключены. Текущая реализация использует асинхронный FaceitAPIClient
на базе aiohttp и требует отдельных тестов.
"""

from typing import Any, Dict

import aiohttp
import pytest

from src.server.exceptions import (
    FaceitAPIError,
    FaceitAPIKeyMissingError,
    PlayerNotFoundError,
    RateLimitExceededError,
)
from src.server.integrations.faceit_client import FaceitAPIClient


pytestmark = pytest.mark.asyncio


class _DummyResponse:
    def __init__(
        self,
        status: int,
        json_data: Dict[str, Any] | None = None,
        text_data: str = "",
    ) -> None:
        self.status = status
        self._json = json_data or {}
        self._text = text_data

    async def __aenter__(self) -> "_DummyResponse":
        return self

    async def __aexit__(self, exc_type, exc, tb) -> bool:  # noqa: ANN001, ANN003
        return False

    async def json(self) -> Dict[str, Any]:
        return self._json

    async def text(self) -> str:
        return self._text


class _DummySession:
    def __init__(self, response_or_error: Any) -> None:
        self._response_or_error = response_or_error

    async def __aenter__(self) -> "_DummySession":
        return self

    async def __aexit__(self, exc_type, exc, tb) -> bool:  # noqa: ANN001, ANN003
        return False

    def get(self, *args: Any, **kwargs: Any):  # noqa: ANN002, ANN003
        if isinstance(self._response_or_error, Exception):
            raise self._response_or_error
        return self._response_or_error


async def _patch_client_session(monkeypatch: pytest.MonkeyPatch, response: Any) -> None:
    import src.server.integrations.faceit_client as faceit_client_module

    monkeypatch.setattr(
        faceit_client_module.aiohttp,
        "ClientSession",
        lambda *args, **kwargs: _DummySession(response),  # noqa: ARG005
    )


class TestFaceitAPIClient:
    async def test_get_player_success(self, monkeypatch: pytest.MonkeyPatch) -> None:
        player_payload = {
            "player_id": "test-player-123",
            "nickname": "test_player",
            "country": "RU",
            "games": {"cs2": {"skill_level": 7, "faceit_elo": 1500}},
        }
        response = _DummyResponse(status=200, json_data=player_payload)
        await _patch_client_session(monkeypatch, response)

        client = FaceitAPIClient(api_key="test_key")
        result = await client.get_player_by_nickname("test_player")

        assert result == player_payload

    async def test_get_player_not_found(self, monkeypatch: pytest.MonkeyPatch) -> None:
        response = _DummyResponse(status=404, json_data={})
        await _patch_client_session(monkeypatch, response)

        client = FaceitAPIClient(api_key="test_key")

        with pytest.raises(PlayerNotFoundError):
            await client.get_player_by_nickname("unknown_player")

    async def test_get_player_rate_limit(self, monkeypatch: pytest.MonkeyPatch) -> None:
        response = _DummyResponse(status=429, json_data={})
        await _patch_client_session(monkeypatch, response)

        client = FaceitAPIClient(api_key="test_key")

        with pytest.raises(RateLimitExceededError):
            await client.get_player_by_nickname("any_player")

    async def test_get_player_missing_api_key(self, monkeypatch: pytest.MonkeyPatch) -> None:
        import src.server.integrations.faceit_client as faceit_client_module

        monkeypatch.setattr(
            faceit_client_module.settings,
            "FACEIT_API_KEY",
            None,
            raising=False,
        )

        client = FaceitAPIClient(api_key=None)

        with pytest.raises(FaceitAPIKeyMissingError):
            await client.get_player_by_nickname("any_player")

    async def test_get_player_network_error(self, monkeypatch: pytest.MonkeyPatch) -> None:
        error = aiohttp.ClientError("boom")
        await _patch_client_session(monkeypatch, error)

        client = FaceitAPIClient(api_key="test_key")

        with pytest.raises(FaceitAPIError) as exc_info:
            await client.get_player_by_nickname("any_player")

        assert "Network error" in str(exc_info.value.detail)

    async def test_get_player_stats_success(self, monkeypatch: pytest.MonkeyPatch) -> None:
        stats_payload = {
            "lifetime": {
                "matches": "150",
                "k_d_ratio": "1.25",
                "Win Rate %": "54.67",
            },
        }
        response = _DummyResponse(status=200, json_data=stats_payload)
        await _patch_client_session(monkeypatch, response)

        client = FaceitAPIClient(api_key="test_key")
        result = await client.get_player_stats("player-id")

        assert result == stats_payload

    async def test_get_player_stats_not_found(self, monkeypatch: pytest.MonkeyPatch) -> None:
        response = _DummyResponse(status=404, json_data={})
        await _patch_client_session(monkeypatch, response)

        client = FaceitAPIClient(api_key="test_key")

        with pytest.raises(FaceitAPIError) as exc_info:
            await client.get_player_stats("player-id")

        assert exc_info.value.status_code == 404
