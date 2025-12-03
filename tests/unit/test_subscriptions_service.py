"""Unit tests for SubscriptionService."""

from datetime import datetime, timedelta

import pytest
from fastapi import HTTPException

from src.server.features.subscriptions.models import SubscriptionTier, UserSubscription
from src.server.features.subscriptions.service import SubscriptionService


@pytest.fixture
def service():
    return SubscriptionService()


@pytest.mark.asyncio
async def test_get_subscription_plans_returns_all_tiers(service):
    plans = await service.get_subscription_plans()

    assert set(plans.keys()) == {
        SubscriptionTier.FREE.value,
        SubscriptionTier.BASIC.value,
        SubscriptionTier.PRO.value,
        SubscriptionTier.ELITE.value,
    }

    pro_plan = plans[SubscriptionTier.PRO.value]
    assert pro_plan.tier is SubscriptionTier.PRO
    assert pro_plan.features.detailed_analysis is True
    assert pro_plan.description


@pytest.mark.asyncio
async def test_get_subscription_plans_error_raises_http_exception(service, monkeypatch):
    # Break internal plans structure to trigger exception path
    monkeypatch.setattr(service, "subscription_plans", None, raising=False)

    with pytest.raises(HTTPException) as exc:
        await service.get_subscription_plans()

    assert exc.value.status_code == 500
    assert "Failed to get subscription plans" in exc.value.detail


@pytest.mark.asyncio
async def test_get_user_subscription_returns_default_data(service):
    subscription = await service.get_user_subscription("user-123")

    assert isinstance(subscription, UserSubscription)
    assert subscription.user_id == "user-123"
    assert subscription.subscription_tier is SubscriptionTier.FREE
    assert subscription.is_active is True
    assert subscription.demos_remaining == 2
    assert subscription.end_date > subscription.start_date


@pytest.mark.asyncio
async def test_create_subscription_uses_plan_configuration(service):
    subscription = await service.create_subscription("u-1", SubscriptionTier.PRO)

    assert subscription.user_id == "u-1"
    assert subscription.subscription_tier is SubscriptionTier.PRO
    assert subscription.is_active is True

    plan = service.subscription_plans[SubscriptionTier.PRO]
    assert subscription.demos_remaining == plan["demos_per_month"]

    delta = subscription.end_date - subscription.start_date
    assert timedelta(days=25) <= delta <= timedelta(days=32)


@pytest.mark.asyncio
async def test_create_subscription_error_raises_http_exception(service, monkeypatch):
    # Remove plan to force KeyError inside create_subscription
    monkeypatch.setattr(service, "subscription_plans", {}, raising=False)

    with pytest.raises(HTTPException) as exc:
        await service.create_subscription("u-1", SubscriptionTier.PRO)

    assert exc.value.status_code == 500
    assert "Failed to create subscription" in exc.value.detail


@pytest.mark.asyncio
async def test_check_feature_access_true_when_plan_allows(service, monkeypatch):
    async def fake_get_user_subscription(user_id: str):  # noqa: ARG001
        now = datetime.utcnow()
        return UserSubscription(
            user_id="u42",
            subscription_tier=SubscriptionTier.ELITE,
            start_date=now,
            end_date=now + timedelta(days=30),
            is_active=True,
            demos_remaining=999,
        )

    monkeypatch.setattr(service, "get_user_subscription", fake_get_user_subscription)

    has_access = await service.check_feature_access("u42", "ai_coach")

    assert has_access is True


@pytest.mark.asyncio
async def test_check_feature_access_false_when_feature_not_in_plan(service, monkeypatch):
    async def fake_get_user_subscription(user_id: str):  # noqa: ARG001
        now = datetime.utcnow()
        return UserSubscription(
            user_id="u1",
            subscription_tier=SubscriptionTier.BASIC,
            start_date=now,
            end_date=now + timedelta(days=30),
            is_active=True,
            demos_remaining=10,
        )

    monkeypatch.setattr(service, "get_user_subscription", fake_get_user_subscription)

    has_access = await service.check_feature_access("u1", "non_existing_feature")

    assert has_access is False


@pytest.mark.asyncio
async def test_check_feature_access_returns_false_on_exception(service, monkeypatch):
    async def fake_get_user_subscription(user_id: str):  # noqa: ARG001
        raise RuntimeError("DB is down")

    monkeypatch.setattr(service, "get_user_subscription", fake_get_user_subscription)

    has_access = await service.check_feature_access("u1", "ai_coach")

    assert has_access is False
