from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ...auth.dependencies import get_current_active_user
from ...database.models import User
from ...database.connection import get_db
from ...middleware.rate_limiter import rate_limiter
from ...services.rate_limit_service import rate_limit_service
from ..teammates.service import TeammateService
from ..teammates.models import TeammateProfile, TeammatePreferences
import logging


logger = logging.getLogger(__name__)
router = APIRouter(prefix="/teammates", tags=["teammates"])

teammate_service = TeammateService()


async def enforce_teammates_rate_limit(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    await rate_limit_service.enforce_user_operation_limit(
        db=db,
        user_id=current_user.id,
        operation="teammates_search",
    )


@router.post("/search", response_model=List[TeammateProfile])
async def search_teammates(
    preferences: TeammatePreferences,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    _: None = Depends(rate_limiter),
    __: None = Depends(enforce_teammates_rate_limit),
):
    """Search teammates based on preferences for the current user."""
    return await teammate_service.find_teammates(
        db=db,
        current_user=current_user,
        preferences=preferences,
    )


@router.put("/preferences", response_model=TeammatePreferences)
async def update_preferences(
    preferences: TeammatePreferences,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Update teammate search preferences for the current user."""
    return await teammate_service.update_preferences(
        db=db,
        current_user=current_user,
        preferences=preferences,
    )
