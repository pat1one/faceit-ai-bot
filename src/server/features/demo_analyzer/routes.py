import logging
from typing import Optional

from fastapi import APIRouter, File, UploadFile, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..demo_analyzer.service import DemoAnalyzer
from ..demo_analyzer.models import DemoAnalysis
from ...auth.dependencies import get_optional_current_user
from ...database.connection import get_db
from ...database.models import User
from ...middleware.rate_limiter import rate_limiter
from ...services.rate_limit_service import rate_limit_service
from ...exceptions import DemoAnalysisException
from ...config.settings import settings

logger = logging.getLogger(__name__)
router = APIRouter(
    prefix="/demo",
    tags=["demo"]
)

demo_analyzer = DemoAnalyzer()


MAX_DEMO_SIZE_MB = settings.MAX_DEMO_FILE_MB
MAX_DEMO_SIZE_BYTES = MAX_DEMO_SIZE_MB * 1024 * 1024
_SNIFF_BYTES = 4096


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

    filename = (demo.filename or "").lower()
    if not filename.endswith(".dem"):
        raise DemoAnalysisException(
            detail="Invalid file format. Only .dem files are supported.",
            error_code="INVALID_FILE_FORMAT",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    # Read file into memory once to check size and basic content, then rewind
    content = await demo.read(MAX_DEMO_SIZE_BYTES + 1)

    if not content:
        raise DemoAnalysisException(
            detail="Empty file. Please upload a valid CS2 demo.",
            error_code="EMPTY_FILE",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    if len(content) > MAX_DEMO_SIZE_BYTES:
        raise DemoAnalysisException(
            detail=f"File too large. Maximum allowed size is {MAX_DEMO_SIZE_MB} MB.",
            error_code="FILE_TOO_LARGE",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    # Very basic content sanity check: reject obviously textual/script files
    sniff = content[:_SNIFF_BYTES]
    lowered_sniff = sniff.lower()
    suspicious_markers = [
        b"<html",
        b"<script",
        b"<?php",
        b"#!/bin/bash",
        b"#!/usr/bin/env",
        b"import os",
        b"import sys",
    ]
    if any(marker in lowered_sniff for marker in suspicious_markers):
        raise DemoAnalysisException(
            detail="Invalid file content. Expected a binary CS2 demo file.",
            error_code="INVALID_FILE_CONTENT",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    # Rewind file so DemoAnalyzer can read it from the beginning
    demo.file.seek(0)

    return await demo_analyzer.analyze_demo(demo, language=language)
