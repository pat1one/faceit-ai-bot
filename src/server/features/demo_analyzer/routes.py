from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from typing import List, Dict
from ..demo_analyzer.service import DemoAnalyzer
from ..demo_analyzer.models import DemoAnalysis
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/demo", tags=["demo"])

demo_analyzer = DemoAnalyzer()

@router.post("/analyze", response_model=DemoAnalysis)
async def analyze_demo(demo: UploadFile = File(...)):
    """
    Анализ демо файла CS2
    """
    if not demo.filename.endswith('.dem'):
        raise HTTPException(
            status_code=400,
            detail="Invalid file format. Only .dem files are supported"
        )
    
    return await demo_analyzer.analyze_demo(demo)