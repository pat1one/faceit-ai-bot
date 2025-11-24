import logging
from typing import Optional

from fastapi import APIRouter, File, UploadFile, Depends
from sqlalchemy.orm import Session

from ..demo_analyzer.service import DemoAnalyzer
from ..demo_analyzer.models import DemoAnalysis
from ...auth.dependencies import get_optional_current_user
from ...database.connection import get_db
from ...database.models import User
from ...middleware.rate_limiter import rate_limiter
from ...services.rate_limit_service import rate_limit_service

logger = logging.getLogger(__name__)
router = APIRouter(
    prefix="/demo",
    tags=["demo"]
)

demo_analyzer = DemoAnalyzer()


async def enforce_demo_analyze_rate_limit(
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user),
):
    if current_user is None:
        return

    await rate_limit_service.enforce_user_operation_limit(
        db=db,
        user_id=current_user.id,
        operation="demo_analyze",
    )


@router.post(
    "/analyze",
    response_model=DemoAnalysis,
    summary="Demo file analysis",
    description=(
        "Analyzes uploaded CS2 demo file and "
        "returns detailed analysis"
    ),
    responses={
        200: {
            "description": "Analysis completed successfully"
        },
        400: {
            "description": "Invalid file",
            "content": {
                "application/json": {
                    "example": {
                        "error": "Invalid file format. Only .dem files are supported",
                        "error_code": "INVALID_FILE_FORMAT"
                    }
                }
            }
        },
        500: {
            "description": "Internal server error"
        }
    }
)
async def analyze_demo(
    demo: UploadFile = File(...),
    language: str = "ru",
    _: None = Depends(rate_limiter),
    __: None = Depends(enforce_demo_analyze_rate_limit),
):
    """
    CS2 demo file analysis

    Accepts demo file in .dem format and returns detailed game analysis,
    including player performance, round analysis and recommendations.
    """
    return await demo_analyzer.analyze_demo(demo, language=language)
