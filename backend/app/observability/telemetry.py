from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor


def setup_telemetry(app):

    print("SETTING UP TELEMETRY")

    # Create resource
    resource = Resource.create({
        "service.name": "ai-backend"
    })

    # Create provider
    provider = TracerProvider(resource=resource)

    # Set provider globally
    trace.set_tracer_provider(provider)

    print("TRACER PROVIDER CREATED")

    # OTLP exporter
    otlp_exporter = OTLPSpanExporter(
        endpoint="http://otel-collector:4318/v1/traces"
    )

    print("OTLP EXPORTER CREATED")

    # Span processor
    span_processor = BatchSpanProcessor(otlp_exporter)

    provider.add_span_processor(span_processor)

    print("SPAN PROCESSOR ATTACHED")

    # Instrument FastAPI
    FastAPIInstrumentor.instrument_app(app)

    print("FASTAPI INSTRUMENTED")

    return trace.get_tracer("ai-backend")