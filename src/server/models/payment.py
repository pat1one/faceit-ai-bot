from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal

class PaymentRequest(BaseModel):
    amount: Decimal = Field(..., gt=0)
    currency: str = Field(..., regex='^[A-Z]{3}$')
    description: str = Field(..., min_length=1, max_length=128)

class PaymentResponse(BaseModel):
    payment_url: str
    status: str
    payment_id: Optional[str] = None

class PaymentStatus(BaseModel):
    status: str
    payment_id: str
    amount: Decimal
    currency: str