"""
OpenAI Integration Service
Service for GPT-4 and other OpenAI models
"""
from typing import Dict, List, Optional
import logging
from openai import AsyncOpenAI
from ..config.settings import settings

logger = logging.getLogger(__name__)


class OpenAIService:
    """Service for OpenAI API"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or getattr(settings, 'OPENAI_API_KEY', None)
        if not self.api_key:
            logger.warning("OpenAI API key not configured")
            self.client = None
        else:
            self.client = AsyncOpenAI(api_key=self.api_key)
    
    async def analyze_player_performance(
        self, 
        stats: Dict,
        match_history: Optional[List[Dict]] = None
    ) -> str:
        """
        Analyze player performance with GPT-4
        
        Args:
            stats: Current player statistics
            match_history: Recent match history
            
        Returns:
            Detailed analysis and recommendations
        """
        if not self.client:
            return "AI analysis unavailable - API key not configured"
        
        try:
            prompt = self._build_analysis_prompt(stats, match_history or [])
            
            response = await self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {
                        "role": "system", 
                        "content": "You are a professional CS2 coach with over 10 years of experience. "
                                 "Analyze player statistics and provide specific, "
                                 "actionable recommendations for improvement."
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1500
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            return f"Error analyzing performance: {str(e)}"
    
    async def generate_training_plan(
        self,
        player_stats: Dict,
        focus_areas: List[str]
    ) -> Dict:
        """
        Generate personalized training plan
        
        Args:
            player_stats: Player statistics
            focus_areas: Areas for improvement
            
        Returns:
            Structured training plan
        """
        if not self.client:
            return self._get_default_training_plan()
        
        try:
            prompt = f"""
            Create detailed training plan for CS2 player:
            
            Statistics:
            - K/D: {player_stats.get('kd_ratio', 'N/A')}
            - Headshot %: {player_stats.get('hs_percentage', 'N/A')}
            - Win Rate: {player_stats.get('win_rate', 'N/A')}
            
            Focus on: {', '.join(focus_areas)}
            
            Return JSON with fields: daily_exercises, weekly_goals, estimated_time
            """
            
            response = await self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": "You are a CS2 coach. Reply only in JSON format."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=1000
            )
            
            import json
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            logger.error(f"Error generating training plan: {str(e)}")
            return self._get_default_training_plan()
    
    def _build_analysis_prompt(self, stats: Dict, match_history: List[Dict]) -> str:
        """Build analysis prompt"""
        return f"""
        Analyze CS2 player statistics:
        
        Current metrics:
        - K/D Ratio: {stats.get('kd_ratio', 'N/A')}
        - Headshot %: {stats.get('hs_percentage', 'N/A')}
        - Win Rate: {stats.get('win_rate', 'N/A')}
        - Avg Damage: {stats.get('avg_damage', 'N/A')}
        - Matches Played: {stats.get('matches_played', 'N/A')}
        
        Recent match history: {len(match_history)} matches
        
        Provide detailed analysis:
        1. Strengths
        2. Weaknesses
        3. Specific recommendations for improvement
        4. Action plan for the next week
        """
    
    def _get_default_training_plan(self) -> Dict:
        """Default training plan"""
        return {
            "daily_exercises": [
                {
                    "name": "Aim Training",
                    "duration": 30,
                    "description": "Aim training on aim_botz"
                },
                {
                    "name": "Spray Control",
                    "duration": 20,
                    "description": "Recoil control for AK-47 and M4A4"
                }
            ],
            "weekly_goals": [
                "Increase accuracy by 5%",
                "Improve K/D to 1.2"
            ],
            "estimated_time": "2-3 weeks"
        }
