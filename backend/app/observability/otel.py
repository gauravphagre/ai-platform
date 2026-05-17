from opentelemetry import trace

# Tracer is set up in telemetry.py
tracer = trace.get_tracer(__name__)
