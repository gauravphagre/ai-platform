"""Loki LogQL query templates."""

# Examples (LogQL)
ERROR_LOGS_LAST_5M = '{level="error"} |= ""'
WARN_LOGS_LAST_5M = '{level="warn"} |= ""'


def service_errors(service: str) -> str:
    # Assumes logs have label {service="..."}
    return f'{{service="{service}", level="error"}}'


def service_logs(service: str) -> str:
    return f'{{service="{service}"}}'

