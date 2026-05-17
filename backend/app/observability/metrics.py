from prometheus_client import Counter, Histogram
import time

CHAT_REQUESTS = Counter(
    "chat_requests_total",
    "Total chat requests"
)

CHAT_LATENCY = Histogram(
    "chat_latency_seconds",
    "Chat request latency"
)

TOKEN_USAGE = Counter(
    "chat_tokens_total",
    "Tokens generated"
)

def count_tokens(response):
    tokens = len(response.split())
    TOKEN_USAGE.inc(tokens)
    return tokens

def track_latency(start):
    duration = time.time() - start
    CHAT_LATENCY.observe(duration)
    return duration