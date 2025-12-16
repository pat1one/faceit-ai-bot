"""
Validators for demo analysis
"""
from pydantic import BaseModel, field_validator
from typing import Optional


class DemoFileValidator(BaseModel):
    """Validator for demo files"""
    filename: str
    content_type: str
    size: int

    @field_validator("filename")
    @classmethod
    def validate_filename(cls, v: str) -> str:
        if not v or not v.endswith(".dem"):
            raise ValueError("Only .dem files are supported")
        return v

    @field_validator("size")
    @classmethod
    def validate_size(cls, v: int) -> int:
        max_size = 100 * 1024 * 1024  # 100MB
        if v > max_size:
            raise ValueError(
                f"File size exceeds maximum of {max_size} bytes (100MB)"
            )
        if v <= 0:
            raise ValueError("File size must be greater than 0")
        return v

    @field_validator("content_type")
    @classmethod
    def validate_content_type(cls, v: str) -> str:
        allowed_types = [
            "application/octet-stream",
            "application/x-demo",
            "application/demo",
        ]
        if v and v not in allowed_types:
            # Not strict validation, as browsers may send different types
            pass
        return v

