"""Unit tests for payments routes"""

from unittest.mock import Mock, AsyncMock

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.server.features.payments.routes import (
    router,
    get_payment_service,
)
from src.server.features.payments.models import REGION_PAYMENT_CONFIG, PaymentProvider
from src.server.config.settings import settings


@pytest.fixture
def app():
    """FastAPI app with payments router only."""
    # Ensure test mode so webhooks skip strict auth/signature checks
    settings.TEST_ENV = True
    app = FastAPI()
    app.include_router(router)
    return app


@pytest.fixture
def mock_payment_service():
    service = Mock()
    service.process_webhook = AsyncMock()
    return service


@pytest.fixture
def client(app, mock_payment_service):
    app.dependency_overrides[get_payment_service] = lambda: mock_payment_service

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


def test_get_payment_methods_ru(client):
    """Should return RegionPaymentMethods config for RU region."""
    response = client.get("/payments/methods/RU")

    assert response.status_code == 200
    data = response.json()
    assert data["region"] == "RU"
    assert len(data["available_methods"]) == len(
        REGION_PAYMENT_CONFIG["RU"].available_methods
    )


def test_get_payment_methods_unsupported_region(client):
    response = client.get("/payments/methods/UNKNOWN")

    assert response.status_code == 400


def test_sbp_webhook_success(client, mock_payment_service):
    payload = {"payment_id": "sbp123"}

    response = client.post("/payments/webhook/sbp", json=payload)

    assert response.status_code == 200
    mock_payment_service.process_webhook.assert_awaited_once()
    args, _ = mock_payment_service.process_webhook.call_args
    assert args[0] == PaymentProvider.SBP
    assert args[1]["payment_id"] == "sbp123"


def test_yookassa_webhook_success(client, mock_payment_service):
    payload = {"object": {"id": "yk1"}}

    response = client.post("/payments/webhook/yookassa", json=payload)

    assert response.status_code == 200
    mock_payment_service.process_webhook.assert_awaited()
    args, _ = mock_payment_service.process_webhook.call_args
    assert args[0] == PaymentProvider.YOOKASSA


def test_qiwi_webhook_success(client, mock_payment_service):
    payload = {"payment": {"id": "q1"}}

    response = client.post("/payments/webhook/qiwi", json=payload)

    assert response.status_code == 200
    mock_payment_service.process_webhook.assert_awaited()
    args, _ = mock_payment_service.process_webhook.call_args
    assert args[0] == PaymentProvider.QIWI


def test_sbp_webhook_requires_signature_when_not_test_env(client, mock_payment_service, monkeypatch):
    # In non-test environment with SBP_WEBHOOK_SECRET set, missing or invalid signature
    # must result in 401 and no webhook processing.
    monkeypatch.setattr(settings, "TEST_ENV", False, raising=False)
    monkeypatch.setattr(settings, "SBP_WEBHOOK_SECRET", "secret", raising=False)

    payload = {"payment_id": "sbp123"}

    # Missing signature
    response = client.post("/payments/webhook/sbp", json=payload)
    assert response.status_code == 401
    mock_payment_service.process_webhook.assert_not_awaited()

    # Valid signature
    response_ok = client.post(
        "/payments/webhook/sbp",
        json=payload,
        headers={"Signature": "secret"},
    )
    assert response_ok.status_code == 200
    mock_payment_service.process_webhook.assert_awaited()


def test_yookassa_webhook_requires_valid_auth_when_not_test_env(client, mock_payment_service, monkeypatch):
    # In non-test environment, YooKassa webhook must validate Authorization header.
    monkeypatch.setattr(settings, "TEST_ENV", False, raising=False)
    monkeypatch.setattr(settings, "YOOKASSA_SHOP_ID", "shop", raising=False)
    monkeypatch.setattr(settings, "YOOKASSA_SECRET_KEY", "secret", raising=False)

    payload = {"object": {"id": "yk1"}}

    # Missing Authorization header -> 401
    response = client.post("/payments/webhook/yookassa", json=payload)
    assert response.status_code == 401
    mock_payment_service.process_webhook.assert_not_awaited()

    # Wrong Authorization header -> 401
    response_bad = client.post(
        "/payments/webhook/yookassa",
        json=payload,
        headers={"Authorization": "Basic wrong"},
    )
    assert response_bad.status_code == 401
    mock_payment_service.process_webhook.assert_not_awaited()

    # Correct Authorization header -> 200 and webhook processed
    import base64

    credentials = "shop:secret"
    expected = "Basic " + base64.b64encode(credentials.encode("utf-8")).decode("utf-8")

    response_ok = client.post(
        "/payments/webhook/yookassa",
        json=payload,
        headers={"Authorization": expected},
    )
    assert response_ok.status_code == 200
    mock_payment_service.process_webhook.assert_awaited()
