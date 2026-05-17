FROM grafana/k6:latest

WORKDIR /app

COPY load-test.js .

CMD ["run", "/app/load-test.js"]