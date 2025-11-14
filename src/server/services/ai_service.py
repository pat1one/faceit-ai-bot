"""AI Service for player analysis"""
import logging
from typing import Dict, List

logger = logging.getLogger(__name__)


class AIService:
    """AI analysis service with enhanced rule-based analysis"""

    def __init__(self):
        logger.info("AI Service initialized")

    async def analyze_player_with_ai(
        self,
        nickname: str,
        stats: Dict,
        match_history: List[Dict],
        language: str = "ru"
    ) -> Dict[str, any]:
        """Analyze player with enhanced rule-based analysis"""
        logger.info(f"Analyzing player {nickname}")
        return self._get_analysis(stats, nickname, language)

    def generate_training_plan(
        self,
        nickname: str,
        stats: Dict,
        language: str = "ru"
    ) -> Dict:
        """Generate personalized training plan for player"""
        kd = float(stats.get("kd_ratio", 1.0))
        win_rate = float(stats.get("win_rate", 50.0))
        
        if language == "en":
            plan = {
                "player": nickname,
                "duration": "4 weeks",
                "focus_areas": ["Aim training", "Map control", "Positioning"],
                "daily_routine": [
                    "Aim practice: 30 minutes",
                    "Demo review: 20 minutes",
                    "Competitive matches: 2-3 hours"
                ],
                "weekly_goals": [
                    "Week 1: Improve aim consistency",
                    "Week 2: Master 2 maps",
                    "Week 3: Improve game sense",
                    "Week 4: Competitive play"
                ]
            }
        else:
            plan = {
                "player": nickname,
                "duration": "4 недели",
                "focus_areas": ["Тренировка прицеливания", "Контроль карты", "Позиционирование"],
                "daily_routine": [
                    "Тренировка прицеливания: 30 минут",
                    "Разбор демо: 20 минут",
                    "Соревновательные матчи: 2-3 часа"
                ],
                "weekly_goals": [
                    "Неделя 1: Улучшить консистентность прицеливания",
                    "Неделя 2: Освоить 2 карты",
                    "Неделя 3: Улучшить игровое чутье",
                    "Неделя 4: Соревновательная игра"
                ]
            }
        
        return plan

    def _get_analysis(
        self,
        stats: Dict,
        nickname: str = "Player",
        language: str = "ru"
    ) -> Dict:
        """Enhanced rule-based analysis"""
        kd = float(stats.get("kd_ratio", 1.0))
        win_rate = float(stats.get("win_rate", 50.0))

        # Scoring system
        aim_score = min(10, max(1, int(kd * 4)))
        game_sense_score = min(10, max(1, int(win_rate / 10)))

        # Analysis based on performance
        if language == "en":
            analysis_text = f"{nickname} shows K/D {kd:.2f}"
            tier = "intermediate"
            areas = ["aiming"]
            recs = ["Practice daily"]
            time_est = "2-4 weeks"
        else:
            analysis_text = f"{nickname} показывает K/D {kd:.2f}"
            tier = "средний"
            areas = ["прицеливание"]
            recs = ["Тренировка ежедневно"]
            time_est = "2-4 недели"

        return {
            "analysis": analysis_text,
            "player_tier": tier,
            "overall_score": int((aim_score + game_sense_score) / 2),
            "strengths": {"aim": aim_score},
            "focus_areas": areas,
            "recommendations": recs,
            "estimated_improvement_time": time_est
        }
