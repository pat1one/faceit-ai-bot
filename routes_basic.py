"""
Basic Analysis API Routes - No dependencies
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, List
from pydantic import BaseModel
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/ai", tags=["ai-analysis"])


class PlayerAnalysisRequest(BaseModel):
    """Player analysis request"""
    player_nickname: str
    faceit_id: str | None = None


class PlayerAnalysisResponse(BaseModel):
    """Player analysis response"""
    player_id: str
    nickname: str
    analysis: str
    recommendations: List[str]
    training_plan: Dict
    strengths: List[str]
    weaknesses: List[str]


@router.post("/analyze-player", response_model=PlayerAnalysisResponse)
async def analyze_player(request: PlayerAnalysisRequest):
    """
    Basic player analysis - works without any dependencies
    """
    try:
        # Mock successful analysis
        player_id = "mock-player-id"
        
        # Simple analysis based on nickname length
        if len(request.player_nickname) > 8:
            analysis = f"Player {request.player_nickname} shows good potential"
            strengths = ["experience", "dedication"]
            weaknesses = ["consistency"]
            recommendations = ["Practice regularly", "Focus on improvement"]
        else:
            analysis = f"Player {request.player_nickname} is developing skills"
            strengths = ["potential", "motivation"]
            weaknesses = ["experience", "technique"]
            recommendations = ["Learn basics", "Practice fundamentals"]

        # Basic training plan
        training_plan = {
            "focus_areas": weaknesses[:2],
            "daily_exercises": [
                {
                    "name": "Practice Session",
                    "duration": "1 hour",
                    "description": "Regular practice",
                    "maps": ["de_mirage", "de_dust2"]
                }
            ],
            "weekly_goals": ["Improve skills", "Gain experience"],
            "estimated_time": "4-6 weeks"
        }

        return PlayerAnalysisResponse(
            player_id=player_id,
            nickname=request.player_nickname,
            analysis=analysis,
            recommendations=recommendations,
            training_plan=training_plan,
            strengths=strengths,
            weaknesses=weaknesses
        )

    except Exception as e:
        logger.error(f"Error analyzing player: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to analyze player"
        )


@router.get("/training-plan/{player_id}")
async def get_training_plan(player_id: str):
    """
    Get basic training plan
    """
    try:
        training_plan = {
            "focus_areas": ["aim", "game_sense"],
            "daily_exercises": [
                {
                    "name": "Practice",
                    "duration": "1 hour",
                    "description": "Daily practice session",
                    "maps": ["training_maps"]
                }
            ],
            "weekly_goals": ["Improve performance"],
            "estimated_time": "4 weeks"
        }

        return training_plan

    except Exception as e:
        logger.error(f"Error generating training plan: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to generate training plan"
        )
