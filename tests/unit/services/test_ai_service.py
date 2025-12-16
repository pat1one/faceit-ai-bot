from typing import Any, Dict, List

import pytest

from src.server.services.ai_service import AIService


pytestmark = pytest.mark.asyncio


class DummyGroqService:
    def __init__(self) -> None:
        self.calls: List[Dict[str, Any]] = []

    async def analyze_player_performance(
        self,
        stats: Dict[str, Any],
        match_history: List[Dict[str, Any]] | None = None,
        language: str = "ru",
    ) -> str:
        self.calls.append(
            {"stats": stats, "match_history": match_history or [], "language": language},
        )
        return (
            "1. Тренируй аим на картах aim_botz и в deathmatch.\n"
            "2. Разбирай свои демо и отмечай типичные ошибки позиционирования.\n"
            "3. Играй соревновательные матчи и работай над командным взаимодействием.\n"
        )


class TestAIServiceAnalyzePlayer:
    async def test_analyze_player_with_ai_combines_scores_and_ai_text(self) -> None:
        service = AIService()
        dummy_groq = DummyGroqService()
        service.groq_service = dummy_groq  # type: ignore[assignment]

        stats: Dict[str, Any] = {
            "kd_ratio": 0.8,
            "win_rate": 42.0,
            "hs_percentage": 35.0,
            "matches_played": 20,
        }
        match_history: List[Dict[str, Any]] = [{"match_id": "m1"}]

        result = await service.analyze_player_with_ai(
            nickname="test_player",
            stats=stats,
            match_history=match_history,
            language="ru",
        )

        assert result["detailed_analysis"].startswith("1.")

        strengths = result["strengths"]
        assert set(strengths.keys()) == {
            "aim",
            "game_sense",
            "positioning",
            "teamwork",
            "consistency",
        }
        for value in strengths.values():
            assert 1 <= value <= 10

        weaknesses = result["weaknesses"]
        assert weaknesses["areas"]
        assert weaknesses["priority"] in weaknesses["areas"]
        assert weaknesses["recommendations"]

        training_plan = result["training_plan"]
        assert isinstance(training_plan, dict)
        assert "daily_exercises" in training_plan
        assert training_plan["daily_exercises"]
        assert "estimated_time" in training_plan

        assert isinstance(result["overall_rating"], int)
        assert 1 <= result["overall_rating"] <= 10

        assert len(dummy_groq.calls) == 1
        groq_call = dummy_groq.calls[0]
        assert groq_call["stats"]["kd_ratio"] == 0.8
        assert groq_call["stats"]["win_rate"] == 42.0

    async def test_generate_training_plan_without_focus_areas_uses_rules(self) -> None:
        service = AIService()

        stats: Dict[str, Any] = {
            "kd_ratio": 0.9,
            "win_rate": 48.0,
            "hs_percentage": 35.0,
        }

        plan = await service.generate_training_plan(
            nickname="test_player",
            stats=stats,
            language="en",
            focus_areas=None,
        )

        assert plan["focus_areas"]
        assert isinstance(plan["daily_exercises"], list)
        assert plan["daily_exercises"]
        assert isinstance(plan["estimated_time"], str)


class TestAIServiceExtractRecommendations:
    def test_extract_ai_recommendations_ru_keeps_cs2_lines(self) -> None:
        service = AIService()

        detailed_text = """
        1. Тренируй аим на aim_botz и в deathmatch, фокусируясь на хедшотах.
        2. Анализируй свои демо и отмечай типичные ошибки позиционирования.
        - Играй соревновательные матчи и работай над командным взаимодействием.
        """

        recs = service._extract_ai_recommendations(
            detailed_text=detailed_text,
            language="ru",
        )

        assert recs
        joined = " ".join(recs)
        assert "aim_botz" in joined or "демо" in joined

    def test_extract_ai_recommendations_ignores_non_cs2_text(self) -> None:
        service = AIService()

        detailed_text = """
        1. Делай утреннюю зарядку и пробегай несколько километров каждый день.
        2. Занимайся йогой и медитацией перед сном.
        """

        recs = service._extract_ai_recommendations(
            detailed_text=detailed_text,
            language="ru",
        )

        assert recs == []

    def test_extract_ai_recommendations_en_filters_and_keeps_cs2_lines(self) -> None:
        service = AIService()

        detailed_text = """
        1. Practice aim and spray control in deathmatch.
        2. Go for a morning run and do yoga every day.
        3. Review your demos and focus on positioning.
        """

        recs = service._extract_ai_recommendations(
            detailed_text=detailed_text,
            language="en",
        )

        assert recs
        joined = " ".join(recs).lower()
        assert "aim" in joined or "deathmatch" in joined or "demo" in joined
        assert "yoga" not in joined
        assert "run" not in joined


class TestAIServiceTrainingPlanEstimatedTime:
    async def test_generate_training_plan_estimated_time_tiers(self) -> None:
        service = AIService()

        async def check(kd: float, win_rate: float, language: str, expected: str) -> None:
            stats: Dict[str, Any] = {
                "kd_ratio": kd,
                "win_rate": win_rate,
                "hs_percentage": 40.0,
            }

            plan = await service.generate_training_plan(
                nickname="player",
                stats=stats,
                language=language,
                focus_areas=["aim"],
            )

            assert plan["estimated_time"] == expected

        await check(0.8, 40.0, "en", "6 weeks")
        await check(1.0, 50.0, "en", "4 weeks")
        await check(1.3, 60.0, "en", "2-3 weeks")

        await check(0.8, 40.0, "ru", "6 недель")
        await check(1.0, 50.0, "ru", "4 недели")
        await check(1.3, 60.0, "ru", "2-3 недели")

