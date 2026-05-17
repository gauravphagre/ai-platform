import json
import time
import os
import logging

from prometheus_client import Gauge, start_http_server

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("security-exporter")

critical_gauge = Gauge(
    "trivy_critical_vulnerabilities",
    "Critical vulnerabilities",
    ["image"]
)

high_gauge = Gauge(
    "trivy_high_vulnerabilities",
    "High vulnerabilities",
    ["image"]
)

def load_report(path, image):
    if not os.path.exists(path):
        logger.warning(f"Report not found yet: {path}")
        return

    try:
        with open(path) as f:
            data = json.load(f)

        critical = 0
        high = 0

        for result in data.get("Results", []):
            for vuln in result.get("Vulnerabilities", []) or []:

                severity = vuln.get("Severity")

                if severity == "CRITICAL":
                    critical += 1

                elif severity == "HIGH":
                    high += 1

        critical_gauge.labels(image=image).set(critical)
        high_gauge.labels(image=image).set(high)

        logger.info(
            f"{image}: critical={critical}, high={high}"
        )

    except Exception as e:
        logger.error(f"Failed loading {path}: {e}")

start_http_server(9110)

logger.info("Security exporter started on port 9110")

while True:

    load_report("/reports/backend.json", "backend")
    load_report("/reports/frontend.json", "frontend")
    load_report("/reports/ollama.json", "ollama")

    time.sleep(60)