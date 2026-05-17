FROM python:3.11-slim

WORKDIR /app

COPY trivy_metrics.py .

RUN pip install prometheus_client

CMD ["python", "trivy_metrics.py"]