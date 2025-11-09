from fastapi import APIRouter, Depends, File, UploadFile
from typing import List, Dict
from ..demo_analyzer.service import DemoAnalyzer
from ..demo_analyzer.models import DemoAnalysis
import logging
import sys
from pathlib import Path

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent.parent))
from exceptions import DemoAnalysisException

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/demo", tags=["demo"])

demo_analyzer = DemoAnalyzer()

@router.post(
    "/analyze",
    response_model=DemoAnalysis,
    summary="Demo file analysis",
    description="Analyzes uploaded CS2 demo file and returns detailed analysis",
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
async def analyze_demo(demo: UploadFile = File(...)):
    """
    CS2 demo file analysis
    
    Accepts demo file in .dem format and returns detailed game analysis,
    including player performance, round analysis and recommendations.
    """
    return await demo_analyzer.analyze_demo(demo)