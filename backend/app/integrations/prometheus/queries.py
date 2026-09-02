"""Prometheus query templates.

Keep PromQL strings centralized here so workflows/services can reuse them.
"""

# Common latency/error queries (examples)
HTTP_REQUEST_RATE_5M = "sum(rate(http_requests_total[5m])) by (service)"
HTTP_ERROR_RATE_5M = "sum(rate(http_requests_total{status=~'5..'}[5m])) by (service)"
LATENCY_P99_5M = "histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m])) by (le, service))"
CPU_USAGE_5M = "avg(rate(process_cpu_seconds_total[5m])) by (service)"
MEMORY_RSS = "avg(process_resident_memory_bytes) by (service)"


def service_error_rate(service: str) -> str:
    return (
        "sum(rate(http_requests_total{service='" + service + "',status=~'5..'}[5m])) "
        "/ sum(rate(http_requests_total{service='" + service + "'}[5m]))"
    )


def service_latency_p99(service: str) -> str:
    return (
        "histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket{service='"
        + service
        + "'}[5m])) by (le))"
    )

