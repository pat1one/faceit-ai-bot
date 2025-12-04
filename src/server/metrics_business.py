"""Business Prometheus metrics for player analysis and users."""

from prometheus_client import Counter, Histogram


ANALYSIS_REQUESTS = Counter(
    "faceit_analysis_requests_total",
    "Total analysis requests",
)


ANALYSIS_DURATION = Histogram(
    "faceit_analysis_duration_seconds",
    "Analysis duration in seconds",
)


ACTIVE_USERS = Counter(
    "faceit_active_users",
    "Active user sessions",
)
