from fastapi import APIRouter, Depends, File, UploadFile
from ..services.ml import MLService
from ..services.payment import PaymentService
from ..models.payment import PaymentRequest, PaymentResponse
import logging

logger = logging.getLogger(__name__)

# Create routers
demo_router = APIRouter(prefix="/demo", tags=["demo"])
payment_router = APIRouter(prefix="/payments", tags=["payments"])
voice_router = APIRouter(prefix="/voice", tags=["voice"])

# Services
ml_service = MLService()
payment_service = PaymentService()

@demo_router.post("/analyze")
async def analyze_demo(demo: UploadFile = File(...)):
    """Analyze CS2 demo using ML model"""
    return await ml_service.analyze_demo(demo)

@payment_router.post("/yookassa", response_model=PaymentResponse)
async def create_yookassa_payment(payment: PaymentRequest):
    """Create payment via YooKassa"""
    return await payment_service.create_yookassa_payment(payment)

@voice_router.get("/commands")
async def get_voice_commands():
    """Get available voice commands"""
    return {
        "available_commands": [
            {"command": "analyze round", "description": "Анализ текущего раунда"},
            {"command": "team strategy", "description": "Рекомендации по командной тактике"},
            {"command": "economy advice", "description": "Советы по экономике"},
            {"command": "position check", "description": "Проверка позиции"},
            {"command": "utility usage", "description": "Советы по использованию утилит"}
        ],
        "languages_supported": ["ru", "en"],
        "status": "active"
    }