import json
import time

def log_event(event: str, data: dict):
    log = {
        "event": event,
        "timestamp": time.time(),
        "data": data
    }
    print(json.dumps(log))