from enum import Enum
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class SubscriptionTier(str, Enum):
    FREE = "free"
    BASIC = "basic"
    PRO = "pro"
    ELITE = "elite"

class SubscriptionFeatures(BaseModel):
    demos_per_month: int
    detailed_analysis: bool
    teammate_search: bool
    custom_recommendations: bool
    priority_support: bool
    ai_coach: bool
    team_analysis: bool

class Subscription(BaseModel):
    tier: SubscriptionTier
    price: float
    currency: str = "USD"
    features: SubscriptionFeatures
    description: str

class UserSubscription(BaseModel):
    user_id: str
    subscription_tier: SubscriptionTier
    start_date: datetime
    end_date: datetime
    is_active: bool
    demos_remaining: int
