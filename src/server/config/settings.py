from pydantic import BaseModel
from functools import lru_cache
import os
from typing import List, Optional

class Settings(BaseModel):
    # App settings
    APP_TITLE: str = "Faceit AI Bot Service"
    APP_VERSION: str = "0.2.0"
    NODE_ENV: str = "production"
    REPLIT_DEV_DOMAIN: Optional[str] = None
    
    # Payment settings
    WEBSITE_URL: str = "http://localhost:3000"
    API_URL: str = "http://localhost:8000"
    
    # СБП API settings
    SBP_TINKOFF_API_URL: str = "https://securepay.tinkoff.ru/v2"
    SBP_TINKOFF_TOKEN: Optional[str] = None
    SBP_TINKOFF_TERMINAL_KEY: Optional[str] = None
    
    SBP_SBERBANK_API_URL: str = "https://api.sberbank.ru/qr"
    SBP_SBERBANK_TOKEN: Optional[str] = None
    
    SBP_VTB_API_URL: str = "https://api.vtb.ru/qr"
    SBP_VTB_TOKEN: Optional[str] = None
    
    SBP_ALPHA_API_URL: str = "https://alfabank.ru/api"
    SBP_ALPHA_TOKEN: Optional[str] = None
    
    # Stripe settings (для международных карт)
    STRIPE_API_URL: str = "https://api.stripe.com"
    STRIPE_SECRET_KEY: Optional[str] = None
    STRIPE_PUBLISHABLE_KEY: Optional[str] = None
    
    # Crypto settings (Binance API)
    BINANCE_API_KEY: Optional[str] = None
    BINANCE_SECRET_KEY: Optional[str] = None
    
    # Stripe settings (для нероссийских платежей)
    STRIPE_API_URL: str = "https://api.stripe.com"
    STRIPE_SECRET_KEY: Optional[str] = None
    STRIPE_PUBLISHABLE_KEY: Optional[str] = None
    
    # PayPal settings (для нероссийских платежей)
    PAYPAL_API_URL: str = "https://api.paypal.com"
    PAYPAL_CLIENT_ID: Optional[str] = None
    PAYPAL_SECRET_KEY: Optional[str] = None
    
    # Crypto settings
    CRYPTO_API_URL: str = "https://api.crypto.com"
    CRYPTO_API_KEY: Optional[str] = None
    CRYPTO_SECRET_KEY: Optional[str] = None

    # CORS settings
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:4000",
        "http://localhost:8000",
        "https://89f4cd76-9b36-4cb9-9797-f7bf95690841-00-3isporgvi3p56.picard.replit.dev",
    ]

    # Payment settings
    YOOKASSA_API_URL: str = "https://api.yookassa.ru/v3/payments"
    YOOKASSA_SHOP_ID: Optional[str] = None
    YOOKASSA_SECRET_KEY: Optional[str] = None

    # SBP settings
    SBP_API_URL: Optional[str] = None
    SBP_TOKEN: Optional[str] = None

    # Test settings
    TEST_ENV: bool = False

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()