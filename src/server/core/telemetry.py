"""OpenTelemetry configuration for distributed tracing.

In the production image, OpenTelemetry may not be installed. In this case
telemetry should be disabled gracefully without crashing the application.
"""

import logging
from typing import Any

try:
    from opentelemetry import trace, metrics
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor
    from opentelemetry.sdk.metrics import MeterProvider
    from opentelemetry.exporter.jaeger.thrift import JaegerExporter
    from opentelemetry.exporter.prometheus import PrometheusMetricReader
    from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
    from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
    from opentelemetry.instrumentation.redis import RedisInstrumentor
    from opentelemetry.instrumentation.requests import RequestsInstrumentor
    from opentelemetry.instrumentation.logging import LoggingInstrumentor

    OTEL_AVAILABLE = True
except ImportError:  # opentelemetry is not installed in the environment
    trace = metrics = None  # type: ignore[assignment]
    TracerProvider = BatchSpanProcessor = MeterProvider = None  # type: ignore[assignment]
    JaegerExporter = PrometheusMetricReader = None  # type: ignore[assignment]
    FastAPIInstrumentor = SQLAlchemyInstrumentor = RedisInstrumentor = RequestsInstrumentor = LoggingInstrumentor = None
    OTEL_AVAILABLE = False

from ..config.settings import settings

logger = logging.getLogger(__name__)


def init_telemetry() -> None:
    """Initialize OpenTelemetry tracing and metrics.

    In non-production environments and when OTEL dependencies are missing,
    this function only logs a message and then returns.
    """

    if not settings.ENVIRONMENT == "production":
        logger.info("Telemetry disabled in non-production environment")
        return

    if not OTEL_AVAILABLE:
        logger.info("Telemetry disabled - OpenTelemetry SDK not installed")
        return

    try:
        jaeger_exporter = JaegerExporter(
            agent_host_name=settings.JAEGER_HOST,
            agent_port=settings.JAEGER_PORT,
        )

        trace_provider = TracerProvider()
        trace_provider.add_span_processor(
            BatchSpanProcessor(jaeger_exporter)
        )
        trace.set_tracer_provider(trace_provider)

        prometheus_reader = PrometheusMetricReader()
        meter_provider = MeterProvider(metric_readers=[prometheus_reader])
        metrics.set_meter_provider(meter_provider)

        FastAPIInstrumentor.instrument_app(
            app=None,
            excluded_urls=".*health.*",
        )
        SQLAlchemyInstrumentor().instrument()
        RedisInstrumentor().instrument()
        RequestsInstrumentor().instrument()
        LoggingInstrumentor().instrument()

        logger.info("OpenTelemetry initialized successfully")

    except Exception as e:
        logger.error(f"Failed to initialize OpenTelemetry: {str(e)}")


def get_tracer(name: str) -> Any:
    """Get a tracer instance.

    If OpenTelemetry is not available, a simple no-op stub object is returned.
    """

    if OTEL_AVAILABLE and trace is not None:
        return trace.get_tracer(name)

    class _NoopTracer:
        def __getattr__(self, item: str) -> Any:
            def _noop(*_: Any, **__: Any) -> None:
                return None

            return _noop

    return _NoopTracer()


def get_meter(name: str) -> Any:
    """Get a meter instance.

    If OpenTelemetry is not available, a no-op stub object is returned.
    """

    if OTEL_AVAILABLE and metrics is not None:
        return metrics.get_meter(name)

    class _NoopMeter:
        def __getattr__(self, item: str) -> Any:
            def _noop(*_: Any, **__: Any) -> None:
                return None

            return _noop

    return _NoopMeter()
