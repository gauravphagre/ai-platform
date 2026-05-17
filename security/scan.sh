#!/bin/sh

while true
do
  echo "Starting vulnerability scans..."

  trivy image --scanners vuln \
    --format json \
    -o /reports/backend.json \
    ai-backend

  trivy image --scanners vuln \
    --format json \
    -o /reports/frontend.json \
    ai-frontend

  trivy image --scanners vuln \
    --format json \
    -o /reports/ollama.json \
    ai-ollama

  echo "Scans completed. Sleeping for 1 hour..."

  sleep 3600
done