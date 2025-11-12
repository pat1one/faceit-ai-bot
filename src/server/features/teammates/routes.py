from fastapi import APIRouter
from typing import List
from ..teammates.service import TeammateService
from ..teammates.models import TeammateProfile, TeammatePreferences
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/teammates", tags=["teammates"])

teammate_service = TeammateService()


@router.post("/search", response_model=List[TeammateProfile])
async def search_teammates(preferences: TeammatePreferences, user_id: str):
    """
    Search teammates based on preferences
    """
    return await teammate_service.find_teammates(user_id, preferences)


@router.put("/preferences", response_model=TeammatePreferences)
async def update_preferences(preferences: TeammatePreferences, user_id: str):
    """
    Update teammate search preferences
    """
    return await teammate_service.update_preferences(user_id, preferences)
