"""
Validators for demo analysis
"""
from pydantic import BaseModel, validator
from typing import Optional


class DemoFileValidator(BaseModel):
    """Validator for demo files"""
    filename: str
    content_type: str
    size: int

    @validator('filename')
    def validate_filename(cls, v):
        if not v or not v.endswith('.dem'):
            raise ValueError('Only .dem files are supported')
        return v

    @validator('size')
    def validate_size(cls, v):
        max_size = 100 * 1024 * 1024  # 100MB
        if v > max_size:
            raise ValueError(f'File size exceeds maximum of {max_size} bytes (100MB)')
        if v <= 0:
            raise ValueError('File size must be greater than 0')
        return v

    @validator('content_type')
    def validate_content_type(cls, v):
        allowed_types = ['application/octet-stream', 'application/x-demo', 'application/demo']
        if v and v not in allowed_types:
            # Not strict validation, as browsers may send different types
            pass
        return v

