"""
Security middleware for FastAPI - OWASP compliance
"""
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

# Rate limiting instance
limiter = Limiter(key_func=get_remote_address)

# Rate limit exceeded handler
@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"error": "Too many requests", "retry_after": exc.retry_after}
    )

def setup_security_middleware(app):
    """Setup all security middleware"""

    # Add rate limiting
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    app.add_middleware(SlowAPIMiddleware)

    # Add security headers
    @app.middleware("http")
    async def security_headers(request: Request, call_next):
        response = await call_next(request)

        # OWASP Security Headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self'; style-src 'self'"

        return response

    # Input validation middleware
    @app.middleware("http")
    async def validate_input(request: Request, call_next):
        # Basic input validation
        for param, value in request.query_params.items():
            if len(value) > 1000:  # Protect against oversized input
                raise HTTPException(status_code=400, detail="Parameter too long")

        response = await call_next(request)
        return response

    return app
