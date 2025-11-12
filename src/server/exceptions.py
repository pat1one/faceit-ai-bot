"""
Custom exceptions for application error handling
"""
from fastapi import HTTPException
from typing import Optional


class BaseAPIException(HTTPException):
    """Base API exception"""
    def __init__(self, status_code: int, detail: str, error_code: Optional[str] = None):
        super().__init__(status_code=status_code, detail=detail)
        self.error_code = error_code


class PaymentException(BaseAPIException):
    """Exception during payment processing"""
    def __init__(self, detail: str, error_code: Optional[str] = None):
        super().__init__(status_code=400, detail=detail, error_code=error_code or "PAYMENT_ERROR")


class DemoAnalysisException(BaseAPIException):
    """Exception during demo file analysis"""
    def __init__(self, detail: str, error_code: Optional[str] = None, status_code: int = 400):
        super().__init__(status_code=status_code, detail=detail, error_code=error_code or "DEMO_ANALYSIS_ERROR")


class FaceitAPIException(BaseAPIException):
    """Exception when working with Faceit API"""
    def __init__(self, detail: str, error_code: Optional[str] = None):
        super().__init__(status_code=502, detail=detail, error_code=error_code or "FACEIT_API_ERROR")


class DatabaseException(BaseAPIException):
    """Exception when working with database"""
    def __init__(self, detail: str, error_code: Optional[str] = None):
        super().__init__(status_code=500, detail=detail, error_code=error_code or "DATABASE_ERROR")


class ValidationException(BaseAPIException):
    """Exception during data validation"""
    def __init__(self, detail: str, error_code: Optional[str] = None):
        super().__init__(status_code=422, detail=detail, error_code=error_code or "VALIDATION_ERROR")


class AuthenticationException(BaseAPIException):
    """Authentication exception"""
    def __init__(self, detail: str = "Authentication failed", error_code: Optional[str] = None):
        super().__init__(status_code=401, detail=detail, error_code=error_code or "AUTHENTICATION_ERROR")


class AuthorizationException(BaseAPIException):
    """Authorization exception"""
    def __init__(self, detail: str = "Access denied", error_code: Optional[str] = None):
        super().__init__(status_code=403, detail=detail, error_code=error_code or "AUTHORIZATION_ERROR")

