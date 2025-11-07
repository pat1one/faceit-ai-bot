import requests
from fastapi import HTTPException
import logging
from ..config.settings import settings

logger = logging.getLogger(__name__)

class PaymentService:
    def create_yookassa_payment(self, payment_data):
        if not settings.YOOKASSA_SHOP_ID or not settings.YOOKASSA_SECRET_KEY:
            raise HTTPException(status_code=500, detail="Payment service not configured")

        headers = {"Content-Type": "application/json"}
        auth = (settings.YOOKASSA_SHOP_ID, settings.YOOKASSA_SECRET_KEY)
        data = {
            "amount": {
                "value": f"{payment_data.amount:.2f}",
                "currency": payment_data.currency,
            },
            "confirmation": {
                "type": "redirect",
                "return_url": "http://localhost:3000/payment-success",
            },
            "description": payment_data.description,
        }

        try:
            response = requests.post(
                settings.YOOKASSA_API_URL,
                json=data,
                headers=headers,
                auth=auth,
                timeout=10
            )
            response.raise_for_status()
            payment_data = response.json()
            return {
                "payment_url": payment_data["confirmation"]["confirmation_url"],
                "status": payment_data["status"],
            }
        except requests.Timeout:
            logger.error("YooKassa payment request timeout")
            raise HTTPException(status_code=504, detail="Payment service timeout")
        except requests.RequestException as e:
            logger.error(f"YooKassa payment error: {e}")
            raise HTTPException(status_code=502, detail="Payment service error")

    def create_sbp_payment(self, payment_data):
        if not settings.SBP_API_URL or not settings.SBP_TOKEN:
            raise HTTPException(status_code=500, detail="SBP service not configured")

        # Implement real SBP payment logic here
        return {
            "payment_url": "https://example.com/sbp-payment",
            "status": "pending",
        }

payment_service = PaymentService()