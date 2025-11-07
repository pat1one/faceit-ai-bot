from typing import List, Optional
from fastapi import HTTPException
from ..models import TeammateProfile, PlayerStats, TeammatePreferences
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class TeammateService:
    def __init__(self):
        self.faceit_api_key = None  # Получать из конфигурации
        
    async def find_teammates(
        self,
        user_id: str,
        preferences: TeammatePreferences
    ) -> List[TeammateProfile]:
        """Поиск подходящих тиммейтов на основе предпочтений"""
        try:
            # Получаем статистику пользователя
            user_stats = await self._get_player_stats(user_id)
            
            # Поиск подходящих игроков
            matching_players = await self._find_matching_players(
                user_stats,
                preferences
            )
            
            # Фильтрация и ранжирование результатов
            ranked_players = await self._rank_players(
                matching_players,
                preferences
            )
            
            return ranked_players
            
        except Exception as e:
            logger.exception("Failed to find teammates")
            raise HTTPException(
                status_code=500,
                detail=f"Teammate search failed: {str(e)}"
            )

    async def update_preferences(
        self,
        user_id: str,
        preferences: TeammatePreferences
    ) -> TeammatePreferences:
        """Обновление предпочтений поиска тиммейтов"""
        try:
            # TODO: Сохранение предпочтений в базу данных
            return preferences
        except Exception as e:
            logger.exception("Failed to update preferences")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to update preferences: {str(e)}"
            )

    async def _get_player_stats(self, user_id: str) -> PlayerStats:
        """Получение статистики игрока из FACEIT API"""
        # TODO: Реализовать интеграцию с FACEIT API
        return PlayerStats(
            faceit_elo=2000,
            matches_played=100,
            win_rate=0.55,
            avg_kd=1.2,
            avg_hs=0.65,
            favorite_maps=['de_dust2', 'de_mirage'],
            last_20_matches=[]
        )

    async def _find_matching_players(
        self,
        user_stats: PlayerStats,
        preferences: TeammatePreferences
    ) -> List[TeammateProfile]:
        """Поиск игроков, соответствующих критериям"""
        # TODO: Реализовать поиск по базе данных или API
        return []

    async def _rank_players(
        self,
        players: List[TeammateProfile],
        preferences: TeammatePreferences
    ) -> List[TeammateProfile]:
        """Ранжирование найденных игроков по совместимости"""
        # TODO: Реализовать алгоритм ранжирования
        return sorted(
            players,
            key=lambda x: self._calculate_compatibility_score(x, preferences),
            reverse=True
        )

    def _calculate_compatibility_score(
        self,
        player: TeammateProfile,
        preferences: TeammatePreferences
    ) -> float:
        """Расчет оценки совместимости игрока"""
        # TODO: Реализовать алгоритм оценки совместимости
        return 0.0