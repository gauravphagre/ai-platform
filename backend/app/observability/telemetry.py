from opentelemetry import trace
from opentelemetry.trace import ProxyTracerProvider
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

def setup_telemetry(app):
    current_provider = trace.get_tracer_provider()
    if isinstance(current_provider, ProxyTracerProvider):
        resource = Resource.create({
            "service.name": "ai-backend"
        })
        provider = TracerProvider(resource=resource)
        trace.set_tracer_provider(provider)
        otlp_exporter = OTLPSpanExporter(
            endpoint="http://otel-collector:4318/v1/traces"
        )
        span_processor = BatchSpanProcessor(otlp_exporter)
        provider.add_span_processor(span_processor)
    if not getattr(app, "_is_instrumented_by_opentelemetry", False):
        FastAPIInstrumentor.instrument_app(app)
    return trace.get_tracer("ai-backend")