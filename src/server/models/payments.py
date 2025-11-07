from pydantic import BaseModel, Field, validator

class PaymentRequest(BaseModel):
    amount: float = Field(..., gt=0)
    currency: str = Field(..., min_length=3, max_length=3)
    description: str = Field(..., min_length=1)

    @validator('currency')
    def validate_currency(cls, v):
        allowed_currencies = ['RUB', 'USD', 'EUR']
        if v.upper() not in allowed_currencies:
            raise ValueError(f'Currency must be one of {allowed_currencies}')
        return v.upper()

class PaymentResponse(BaseModel):
    payment_url: str
    status: str