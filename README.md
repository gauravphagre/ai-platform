# 🚀 AI Platform

> A full-stack AI application platform with **chat**, **RAG**, **incident-response workflows**, **conversation history**, **observability**, **security scanning**, and **load testing**.

![Status](https://img.shields.io/badge/status-active-success) ![Backend](https://img.shields.io/badge/backend-FastAPI-009688) ![Frontend](https://img.shields.io/badge/frontend-React-61DAFB) ![Database](https://img.shields.io/badge/database-PostgreSQL-336791) ![Vector%20DB](https://img.shields.io/badge/vector%20db-Qdrant-DC244C) ![Cache](https://img.shields.io/badge/cache-Redis-D82C20) ![LLM](https://img.shields.io/badge/LLM-Ollama-111827)

---

## ✨ What this repository includes

This repository brings together multiple building blocks required for a modern AI application:

- **LLM-powered chat API** with persistent conversation history
- **RAG pipeline** for PDF upload, chunking, embedding, storage, and querying
- **Incident-response workflows** for analysis and remediation flows
- **Observability stack** with Prometheus, Grafana, Loki, Tempo, and OpenTelemetry
- **Security scanning** using Trivy
- **Load testing** using k6
- **Docker-first local development**

---

## 🧱 Architecture Overview

### Core services

| Service | Purpose | Port |
|---|---|---:|
| Frontend | React UI | `3000` |
| Backend | FastAPI API server | `8000` |
| Ollama | Local LLM runtime | `11434` |
| PostgreSQL | Persistent relational storage | `5432` |
| Redis | Cache / worker support | `6379` |
| Qdrant | Vector database for RAG | `6333` |

### Optional profiles

| Profile | Services | Ports |
|---|---|---|
| `observability` | Prometheus, Grafana, Loki, Tempo | `9090`, `3001`, `3100`, `3200` |
| `security` | Trivy, security exporter | `9110` |
| `loadtest` | k6 load tester | internal |

---

## 🛠 Tech Stack

### Backend
- **FastAPI**
- **SQLAlchemy (async)**
- **PostgreSQL**
- **Redis**
- **Qdrant**
- **OpenTelemetry**
- **Prometheus metrics**
- **LangGraph**
- **Ollama / OpenAI-compatible integrations**

### Frontend
- **React 18**
- **React Markdown**
- **Tailwind CSS**

### Platform / Ops
- **Docker Compose**
- **Grafana + Prometheus + Loki + Tempo**
- **Trivy**
- **k6**

---

## 📂 Repository Structure

```text
ai-platform/
├── backend/          # FastAPI app, agents, workflows, services, repositories
├── frontend/         # React frontend
├── observability/    # Prometheus, Grafana, Tempo, OTEL configs
├── security/         # Trivy scanning and exporter
├── load-test/        # k6 load testing scripts
├── ollama/           # Ollama container setup
├── data/             # Persistent local data
└── docker-compose.yml
```

---

## ✅ Prerequisites

Before running the project, make sure you have:

- **Docker** installed
- **Docker Compose** available
- **NVIDIA runtime support** if you want GPU-backed Ollama execution
  - The compose file uses `runtime: nvidia` for the Ollama service
- Enough disk space for models, containers, and local volumes

---

## ⚙️ Configuration

The backend reads settings from environment variables and `.env`.

Important defaults found in the codebase:

| Variable | Default |
|---|---|
| `APP_NAME` | `ai-platform` |
| `DEBUG` | `True` |
| `DATABASE_URL` | `postgresql+asyncpg://ai_user:ai_password@postgres:5432/ai_platform` |
| `OLLAMA_BASE_URL` | `http://ollama:11434` |
| `DEFAULT_MODEL` | `qwen2.5-coder:7b` |

The root `docker-compose.yml` expects a `.env` file via `env_file: .env` for backend and worker services.

If you do not already have one, create a `.env` file in the project root with values similar to:

```env
APP_NAME=ai-platform
DEBUG=true
DATABASE_URL=postgresql+asyncpg://ai_user:ai_password@postgres:5432/ai_platform
OLLAMA_BASE_URL=http://ollama:11434
DEFAULT_MODEL=qwen2.5-coder:7b
```

---

## 🚀 Quick Start

### 1) Clone the repository

```bash
git clone <repository-url>
cd ai-platform
```

### 2) Start the core platform

```bash
docker-compose up --build
```

This starts the main stack:
- `ollama`
- `backend`
- `worker`
- `frontend`
- `postgres`
- `redis`
- `qdrant`

### 3) Open the apps

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **Backend health:** http://localhost:8000/health
- **Metrics:** http://localhost:8000/metrics
- **Qdrant:** http://localhost:6333
- **Ollama:** http://localhost:11434

---

## 👀 How to check if services are up

### Check container status

```bash
docker-compose ps
```

You should see containers in an **Up** or **healthy** state.

### Check logs for a specific service

```bash
docker-compose logs backend
```

Other useful examples:

```bash
docker-compose logs frontend
docker-compose logs ollama
docker-compose logs postgres
docker-compose logs qdrant
```

### Check backend health endpoints

Open these in your browser or API client:

- `http://localhost:8000/health`
- `http://localhost:8000/health/live`
- `http://localhost:8000/health/ready`
- `http://localhost:8000/`

Expected responses include values like:
- `{"status":"healthy"}`
- `{"status":"ok"}`

### Check Docker healthchecks

The compose setup includes healthchecks for:
- **Ollama**
- **Backend**
- **PostgreSQL**
- **Redis**
- **Qdrant**

If a service is failing, inspect logs first and verify dependent services are available.

---

## 🧪 Run optional stacks

### Observability profile

```bash
docker-compose --profile observability up --build
```

Available endpoints:
- **Prometheus:** http://localhost:9090
- **Grafana:** http://localhost:3001
- **Loki:** http://localhost:3100
- **Tempo:** http://localhost:3200

### Security profile

```bash
docker-compose --profile security up --build
```

This enables:
- **Trivy** image scanning
- **Security exporter** on `http://localhost:9110`

### Load testing profile

```bash
docker-compose --profile loadtest up --build
```

This runs the bundled **k6** load test against the backend chat endpoint.

---

## 🔌 Main API Endpoints

### Health

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/` | Basic root status |
| `GET` | `/health` | Health check |
| `GET` | `/health/live` | Liveness probe |
| `GET` | `/health/ready` | Readiness probe |
| `GET` | `/metrics` | Prometheus metrics |

### Chat

| Method | Endpoint | Purpose |
|---|---|---|
| `POST` | `/chat` | Standard chat completion |
| `POST` | `/chat/stream` | Streaming chat response |

### Conversations

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/conversations/` | List all conversations |
| `GET` | `/conversations/{conversation_id}` | Get messages for a conversation |

### RAG

| Method | Endpoint | Purpose |
|---|---|---|
| `POST` | `/rag/upload` | Upload a PDF for ingestion |
| `POST` | `/rag/query` | Query ingested document context |

### Workflows

| Method | Endpoint | Purpose |
|---|---|---|
| `POST` | `/workflows/incidents/create` | Create and run incident workflow |
| `GET` | `/workflows/incidents/{workflow_id}` | Get workflow status |
| `POST` | `/workflows/incidents/{workflow_id}/approve` | Approve remediation action |

---

## 💬 Example capabilities

### Chat
- Stores conversation history in PostgreSQL
- Supports conversation continuation using `conversation_id`
- Uses the configured default model when no model is provided

### RAG flow
1. Upload a PDF
2. Extract text
3. Chunk content
4. Generate embeddings
5. Store vectors in Qdrant
6. Query relevant chunks
7. Generate grounded answers from retrieved context

### Incident workflows
- Create incident records
- Analyze root cause
- Suggest remediation actions
- Approve selected remediation
- Persist workflow state

---

## 📊 Observability

This repo includes observability support for metrics, traces, and logs.

### Included components
- **Prometheus** for metrics
- **Grafana** for dashboards
- **Loki** for logs
- **Tempo** for traces
- **OpenTelemetry Collector** in `observability/docker-compose.yml`

### Backend observability features
- `/metrics` endpoint for Prometheus scraping
- OpenTelemetry setup in the backend app lifecycle
- Logging around chat and workflow events

### Dashboards
Prebuilt dashboards are available under:
- `observability/dashboards/`

---

## 🔐 Security Scanning

Security scanning is powered by **Trivy**.

The scan script continuously scans these images:
- `ai-backend`
- `ai-frontend`
- `ai-ollama`

Reports are written to:
- `security/trivy/reports/`

The security exporter exposes metrics from generated reports.

---

## 📈 Load Testing

The repository includes a **k6** script in `load-test/load-test.js`.

Current test characteristics:
- `5` virtual users
- `20` iterations
- `30s` duration
- Thresholds for failure rate and latency

The load test targets:
- `POST http://backend:8000/chat`

Default model used in the script:
- `qwen2.5-coder:7b`

---

## 🧑‍💻 Local Development Notes

### Backend
- Entry point: `backend/app/main.py`
- Default container command runs:
  - `uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload`
- Python base image: `python:3.11-slim`

### Frontend
- React app served with:
  - `npm start`
- Node base image: `node:20-alpine`

### Backend dependencies include
- `fastapi`
- `uvicorn`
- `sqlalchemy`
- `asyncpg`
- `alembic`
- `qdrant-client`
- `prometheus_client`
- `openai`
- `langgraph`

---

## 🧯 Troubleshooting

### Backend is not starting
- Check whether `postgres`, `redis`, `qdrant`, and `ollama` are running
- Inspect logs:
  ```bash
  docker-compose logs backend
  ```

### Frontend is not loading
- Verify backend is reachable on `http://localhost:8000`
- Check frontend logs:
  ```bash
  docker-compose logs frontend
  ```

### Ollama issues
- Confirm model availability in the Ollama container
- Verify GPU/runtime support if using NVIDIA
- Check logs:
  ```bash
  docker-compose logs ollama
  ```

### Health endpoint fails
- Wait for dependent services to become ready
- Re-run:
  ```bash
  docker-compose ps
  ```

---

## 🛑 Stopping the project

```bash
docker-compose down
```

To also remove volumes:

```bash
docker-compose down -v
```

---

## 📚 Helpful project files

- `docker-compose.yml`
- `backend/app/main.py`
- `backend/app/core/settings.py`
- `backend/app/api/health/health.py`
- `backend/app/api/chat/chat.py`
- `backend/app/api/conversations/conversations.py`
- `backend/app/api/rag/rag.py`
- `backend/app/api/workflows/workflows.py`
- `observability/docker-compose.yml`
- `security/scan.sh`
- `load-test/load-test.js`

---

## 🤝 Summary

If you want a single repository that demonstrates:
- AI chat
- retrieval-augmented generation
- workflow orchestration
- observability
- security scanning
- performance testing

this project gives you all of that in one Docker-based setup.

---

For deeper internal details, also review:
- `CODEBASE_DOCUMENTATION.md`
- `dir_structure.md`

---

## 🧹 Clear Conversation History (API)

You can delete conversation history stored in PostgreSQL via the Conversations API.

> ⚠️ This is a destructive operation (permanent delete).

### Delete **all** conversations

```bash
curl -X DELETE "http://localhost:8000/conversations/?all=true"
```

### Delete the **most recent N** conversations

```bash
# delete most recent 10 conversations
curl -X DELETE "http://localhost:8000/conversations/?n=10"
```

Response example:

```json
{"deleted": 10, "mode": "recent", "n": 10}
```

---

## 🗄️ Database: Quick Test Queries (DBeaver / psql)

If you opened the database in **DBeaver** (or any SQL client), you can use the queries below to validate that conversations and messages are being stored correctly.

```sql
-- 1) List tables in the current schema (usually public)
SELECT table_schema, table_name
FROM information_schema.tables
WHERE table_type = 'BASE TABLE'
  AND table_schema NOT IN ('pg_catalog', 'information_schema')
ORDER BY table_schema, table_name;

-- 2) Show columns for likely tables (adjust names if different)
-- If your tables are named conversations/messages:
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_schema = 'public'
  AND table_name IN ('conversations', 'messages')
ORDER BY table_name, ordinal_position;

-- 3) Count rows
SELECT
  (SELECT COUNT(*) FROM conversations) AS conversations_count,
  (SELECT COUNT(*) FROM messages)       AS messages_count;

-- 4) Most recent 10 conversations
SELECT *
FROM conversations
ORDER BY created_at DESC
LIMIT 10;

-- 5) Messages for the most recent conversation
SELECT m.*
FROM messages m
JOIN conversations c ON c.id = m.conversation_id
ORDER BY c.created_at DESC, m.created_at ASC
LIMIT 200;

-- 6) Messages for a specific conversation
-- Replace :conversation_id with an actual id value
SELECT *
FROM messages
WHERE conversation_id = :conversation_id
ORDER BY created_at ASC;

-- 7) Find conversations with message counts
SELECT
  c.id,
  c.created_at,
  COUNT(m.id) AS message_count
FROM conversations c
LEFT JOIN messages m ON m.conversation_id = c.id
GROUP BY c.id, c.created_at
ORDER BY c.created_at DESC
LIMIT 20;

-- 8) Orphan messages check (should be 0 if FK/cascade is correct)
SELECT COUNT(*) AS orphan_messages
FROM messages m
LEFT JOIN conversations c ON c.id = m.conversation_id
WHERE c.id IS NULL;

-- 9) Search messages containing a keyword
-- Replace 'error' with your term
SELECT *
FROM messages
WHERE content ILIKE '%error%'
ORDER BY created_at DESC
LIMIT 50;

-- 10) Delete test: delete most recent 1 conversation (ONLY if you want to test deletes)
-- Wrap in a transaction so you can ROLLBACK.
BEGIN;

WITH to_delete AS (
  SELECT id
  FROM conversations
  ORDER BY created_at DESC
  LIMIT 1
)
DELETE FROM conversations
WHERE id IN (SELECT id FROM to_delete);

-- Verify counts, then either:
-- ROLLBACK;
-- COMMIT;
```

---
