"""Unit tests for AI analysis routes.

Covers success and error paths of /ai/analyze-player and /ai/training-plan,
plus the internal _parse_analysis helper.
"""

from typing import Any, Dict, List

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.server.middleware.rate_limiter import rate_limiter
import src.server.features.ai_analysis.routes as ai_routes
from src.server.features.ai_analysis.routes import (
    router,
    enforce_ai_player_analysis_rate_limit,
    _parse_analysis,
)


@pytest.fixture
def app() -> FastAPI:
    app = FastAPI()
    app.include_router(router)
    return app


@pytest.fixture
def client(app: FastAPI):
    """TestClient with disabled rate limiting and per-user AI limits."""

    app.dependency_overrides[rate_limiter] = lambda: None
    app.dependency_overrides[enforce_ai_player_analysis_rate_limit] = lambda: None

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()


class DummyFaceitClient:
    def __init__(self, *, player_exists: bool = True, stats_available: bool = True):
        self.player_exists = player_exists
        self.stats_available = stats_available

    async def get_player_by_nickname(self, nickname: str) -> Dict[str, Any] | None:  # noqa: ARG002
        if not self.player_exists:
            return None
        return {"player_id": "player123"}

    async def get_player_stats(self, player_id: str) -> Dict[str, Any] | None:  # noqa: ARG002
        if not self.stats_available:
            return None
        return {
            "lifetime": {
                "K/D Ratio": "1.25",
                "Win Rate %": "55.0",
                "Headshots %": "45.0",
                "Matches": "120",
                "Average K/D Ratio": "1.1",
            }
        }

    async def get_match_history(self, player_id: str, limit: int) -> List[Dict[str, Any]]:  # noqa: ARG002
        return [{"match_id": "m1"}, {"match_id": "m2"}]


class DummyAIService:
    def __init__(self, *, fail_analyze: bool = False, fail_plan: bool = False):
        self.fail_analyze = fail_analyze
        self.fail_plan = fail_plan

    async def analyze_player_with_ai(
        self,
        nickname: str,  # noqa: ARG002
        stats: Dict[str, Any],  # noqa: ARG002
        match_history: List[Dict[str, Any]],  # noqa: ARG002
        language: str = "ru",  # noqa: ARG002
    ) -> Dict[str, Any]:
        if self.fail_analyze:
            raise RuntimeError("analyze error")
        return {
            "detailed_analysis": "Strengths:\n- Good aim\nWeaknesses:\n- Bad eco\nRecommendations:\n- Practice eco",
            "strengths": {"aim": 8, "game_sense": 7},
            "weaknesses": {
                "areas": ["eco"],
                "priority": "eco",
                "recommendations": ["Practice eco"],
            },
        }

    async def generate_training_plan(
        self,
        nickname: str,  # noqa: ARG002
        stats: Dict[str, Any],  # noqa: ARG002
        language: str = "ru",  # noqa: ARG002
    ) -> Dict[str, Any]:
        if self.fail_plan:
            raise RuntimeError("plan error")
        return {
            "focus_areas": ["eco"],
            "daily_exercises": [
                {
                    "name": "Eco practice",
                    "duration": "30 min",
                    "description": "Practice low-buy rounds",
                }
            ],
            "estimated_time": "2-3 weeks",
        }


@pytest.mark.asyncio
async def test_analyze_player_by_nickname_success(client, monkeypatch):
    """Happy path: player found by nickname, stats + history available, AI returns analysis."""

    monkeypatch.setattr(
        ai_routes,
        "FaceitAPIClient",
        lambda: DummyFaceitClient(player_exists=True, stats_available=True),
    )
    monkeypatch.setattr(
        ai_routes,
        "AIService",
        lambda: DummyAIService(),
    )

    response = client.post(
        "/ai/analyze-player",
        json={"player_nickname": "TestNick"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["player_id"] == "player123"
    assert data["nickname"] == "TestNick"
    assert data["analysis"]
    assert data["strengths"]
    assert data["weaknesses"]
    assert data["training_plan"]["focus_areas"] == ["eco"]


@pytest.mark.asyncio
async def test_analyze_player_faceit_id_uses_direct_stats(client, monkeypatch):
    """When faceit_id is provided, route uses it directly without nickname lookup."""

    # Client that ignores nickname and uses provided faceit_id
    class FaceitByIdOnly(DummyFaceitClient):
        async def get_player_by_nickname(self, nickname: str):  # noqa: ARG002
            # Should not be called in this path
            raise AssertionError("get_player_by_nickname should not be used when faceit_id is provided")

    monkeypatch.setattr(
        ai_routes,
        "FaceitAPIClient",
        lambda: FaceitByIdOnly(player_exists=True, stats_available=True),
    )
    monkeypatch.setattr(ai_routes, "AIService", lambda: DummyAIService())

    response = client.post(
        "/ai/analyze-player",
        json={"player_nickname": "Ignored", "faceit_id": "faceit123"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["player_id"] == "faceit123"


@pytest.mark.asyncio
async def test_analyze_player_not_found_returns_404(client, monkeypatch):
    """If player is not found by nickname, route returns 404."""

    monkeypatch.setattr(
        ai_routes,
        "FaceitAPIClient",
        lambda: DummyFaceitClient(player_exists=False, stats_available=True),
    )
    monkeypatch.setattr(ai_routes, "AIService", lambda: DummyAIService())

    response = client.post(
        "/ai/analyze-player",
        json={"player_nickname": "Unknown"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Player not found"


@pytest.mark.asyncio
async def test_analyze_player_stats_not_available_returns_404(client, monkeypatch):
    """If stats are missing, route returns 404."""

    monkeypatch.setattr(
        ai_routes,
        "FaceitAPIClient",
        lambda: DummyFaceitClient(player_exists=True, stats_available=False),
    )
    monkeypatch.setattr(ai_routes, "AIService", lambda: DummyAIService())

    response = client.post(
        "/ai/analyze-player",
        json={"player_nickname": "TestNick"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Stats not available"


@pytest.mark.asyncio
async def test_analyze_player_unexpected_error_returns_500(client, monkeypatch):
    """Unexpected error in AI service should result in 500 response."""

    monkeypatch.setattr(
        ai_routes,
        "FaceitAPIClient",
        lambda: DummyFaceitClient(player_exists=True, stats_available=True),
    )
    monkeypatch.setattr(
        ai_routes,
        "AIService",
        lambda: DummyAIService(fail_plan=True),
    )

    response = client.post(
        "/ai/analyze-player",
        json={"player_nickname": "TestNick"},
    )

    assert response.status_code == 500
    assert response.json()["detail"] == "Failed to analyze player"


@pytest.mark.asyncio
async def test_get_training_plan_success(client, monkeypatch):
    """Happy path for /ai/training-plan/{player_id}."""

    async def get_stats(player_id: str):  # noqa: ARG002
        return {
            "lifetime": {
                "K/D Ratio": "1.2",
                "Win Rate %": "52.0",
                "Headshots %": "43.0",
            }
        }

    async def make_plan(nickname: str, stats: Dict[str, Any]) -> Dict[str, Any]:  # noqa: ARG002
        return {
            "focus_areas": ["aim"],
            "daily_exercises": [],
            "estimated_time": "4 weeks",
        }

    class FaceitForPlan(DummyFaceitClient):
        async def get_player_stats(self, player_id: str):  # noqa: ARG002
            return await get_stats(player_id)

    class AIForPlan(DummyAIService):
        async def generate_training_plan(
            self,
            nickname: str,
            stats: Dict[str, Any],
            language: str = "ru",  # noqa: ARG002
        ) -> Dict[str, Any]:
            return await make_plan(nickname, stats)

    monkeypatch.setattr(ai_routes, "FaceitAPIClient", lambda: FaceitForPlan())
    monkeypatch.setattr(ai_routes, "AIService", lambda: AIForPlan())

    response = client.post("/ai/training-plan/test123")

    assert response.status_code == 200
    data = response.json()
    assert data["focus_areas"] == ["aim"]
    assert data["estimated_time"] == "4 weeks"


@pytest.mark.asyncio
async def test_get_training_plan_stats_not_found_returns_404(client, monkeypatch):
    """If stats are missing, /ai/training-plan should return 404."""

    class NoStatsClient(DummyFaceitClient):
        async def get_player_stats(self, player_id: str):  # noqa: ARG002
            return None

    monkeypatch.setattr(ai_routes, "FaceitAPIClient", lambda: NoStatsClient())
    monkeypatch.setattr(ai_routes, "AIService", lambda: DummyAIService())

    response = client.post("/ai/training-plan/test123")

    assert response.status_code == 404
    assert response.json()["detail"] == "Player stats not found"


@pytest.mark.asyncio
async def test_get_training_plan_unexpected_error_returns_500(client, monkeypatch):
    """Unexpected error in AI service generate_training_plan should yield 500."""

    class StatsOkClient(DummyFaceitClient):
        async def get_player_stats(self, player_id: str):  # noqa: ARG002
            return {
                "lifetime": {
                    "K/D Ratio": "1.2",
                    "Win Rate %": "52.0",
                    "Headshots %": "43.0",
                }
            }

    monkeypatch.setattr(ai_routes, "FaceitAPIClient", lambda: StatsOkClient())
    monkeypatch.setattr(
        ai_routes,
        "AIService",
        lambda: DummyAIService(fail_plan=True),
    )

    response = client.post("/ai/training-plan/test123")

    assert response.status_code == 500
    assert response.json()["detail"] == "Failed to generate training plan"


def test_parse_analysis_extracts_sections_and_items() -> None:
    """_parse_analysis should separate strengths, weaknesses and recommendations."""

    text = """
    Strengths:
    - Good aim
    - Smart rotations

    Weaknesses:
    - Bad economy decisions

    Recommendations:
    - Practice eco rounds
    - Watch pro demos
    """

    strengths, weaknesses, recs = _parse_analysis(text)

    assert "Good aim" in strengths
    assert "Smart rotations" in strengths
    assert "Bad economy decisions" in weaknesses
    assert "Practice eco rounds" in recs
    assert "Watch pro demos" in recs
