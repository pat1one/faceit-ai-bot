"""AI Service for player analysis"""
import logging
from typing import Dict, List, Any

from ..ai.groq_service import GroqService

logger = logging.getLogger(__name__)


class AIService:
    """AI analysis service with enhanced rule-based analysis"""

    def __init__(self):
        self.groq_service = GroqService()
        logger.info("AI Service initialized")

    async def analyze_player_with_ai(
        self,
        nickname: str,
        stats: Dict,
        match_history: List[Dict],
        language: str = "ru"
    ) -> Dict[str, Any]:
        """Analyze player with Groq-backed analysis and structured output"""
        logger.info(f"Analyzing player {nickname}")

        detailed_analysis = await self.groq_service.analyze_player_performance(
            stats=stats,
            match_history=match_history,
        )

        kd = float(stats.get("kd_ratio", 1.0))
        win_rate = float(stats.get("win_rate", 50.0))
        hs_pct = float(stats.get("hs_percentage", 40.0))
        matches = int(stats.get("matches_played", 0))

        aim_score = min(10, int((kd * 4) + (hs_pct / 10)))
        game_sense_score = min(10, int(win_rate / 10))
        positioning_score = min(10, max(5, int(win_rate / 12)))
        teamwork_score = min(10, int((win_rate / 10) + (min(matches, 100) / 20)))
        consistency_score = min(10, int(min(matches, 500) / 50))

        strengths = {
            "aim": max(1, aim_score),
            "game_sense": max(1, game_sense_score),
            "positioning": max(1, positioning_score),
            "teamwork": max(1, teamwork_score),
            "consistency": max(1, consistency_score),
        }

        weaknesses_areas: List[str] = []
        weaknesses_recs: List[str] = []

        if kd < 1.0:
            weaknesses_areas.append("aim")
            weaknesses_recs.append("Practice aiming on training maps")

        if hs_pct < 40:
            weaknesses_areas.append("headshot accuracy")
            weaknesses_recs.append("Focus on headshot-only modes")

        if win_rate < 50:
            weaknesses_areas.append("game sense")
            weaknesses_recs.append("Study professional matches and strategies")

        if matches < 50:
            weaknesses_areas.append("experience")
            weaknesses_recs.append("Play more matches to gain experience")

        if not weaknesses_areas:
            weaknesses_areas = ["consistency"]
            weaknesses_recs = ["Continue maintaining current skill level"]

        priority = weaknesses_areas[0]

        weaknesses = {
            "areas": weaknesses_areas,
            "priority": priority,
            "recommendations": weaknesses_recs,
        }

        training_plan = self.generate_training_plan(
            nickname=nickname,
            stats=stats,
            language=language,
            focus_areas=weaknesses_areas,
        )

        overall_rating = int(
            min(
                10,
                max(
                    1,
                    (
                        aim_score
                        + game_sense_score
                        + positioning_score
                        + teamwork_score
                        + consistency_score
                    )
                    / 5,
                ),
            )
        )

        return {
            "detailed_analysis": detailed_analysis,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "training_plan": training_plan,
            "overall_rating": overall_rating,
        }

    def generate_training_plan(
        self,
        nickname: str,
        stats: Dict,
        language: str = "ru",
        focus_areas: List[str] | None = None,
    ) -> Dict[str, Any]:
        """Generate personalized training plan for player"""
        kd = float(stats.get("kd_ratio", 1.0))
        win_rate = float(stats.get("win_rate", 50.0))

        if focus_areas is None:
            focus_areas = []
            if kd < 1.1:
                focus_areas.append("aim")
            if win_rate < 55:
                focus_areas.append("game sense")
            if not focus_areas:
                focus_areas.append("consistency")

        if language == "en":
            daily_exercises = [
                {
                    "name": "Aim training",
                    "description": "Aim routine on aim_botz and training maps",
                },
                {
                    "name": "Demo review",
                    "description": "Watch and analyze your recent matches",
                },
                {
                    "name": "Competitive matches",
                    "description": "Play 2-3 ranked matches focusing on mistakes",
                },
            ]
            estimated_time = "4 weeks"
        else:
            daily_exercises = [
                {
                    "name": "Тренировка аима",
                    "description": "Рутина на aim_botz и тренировочных картах",
                },
                {
                    "name": "Разбор демо",
                    "description": "Смотреть и разбирать свои последние матчи",
                },
                {
                    "name": "Соревновательные матчи",
                    "description": "Играть 2-3 рейтинговых матча с фокусом на ошибках",
                },
            ]
            estimated_time = "4 недели"

        return {
            "focus_areas": focus_areas,
            "daily_exercises": daily_exercises,
            "estimated_time": estimated_time,
        }
