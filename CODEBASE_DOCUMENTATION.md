# AI-Platform Codebase Documentation

## Overview
AI-Platform is a full-stack local AI application that provides a chat interface powered by Ollama (local LLM), with RAG (Retrieval-Augmented Generation) capabilities, conversation history management, and comprehensive observability through OpenTelemetry.

**Tech Stack:**
- **Backend:** FastAPI (Python) with async/await patterns
- **Frontend:** React 18 with Tailwind CSS and React Markdown
- **LLM:** Ollama (local model: qwen2.5-coder:7b)
- **Database:** PostgreSQL for conversation history
- **Vector Store:** Qdrant for semantic search on documents
- **Observability:** OpenTelemetry with OTLP exporter
- **Monitoring:** Prometheus + Grafana
- **Containerization:** Docker & Docker Compose

---

## Architecture Overview

### Services Architecture
```
┌─────────────────────────────────────────────────────────┐
│                    Frontend (React)                      │
│              :3000 (ModernAIChatUI)                      │
└──────────────────────┬──────────────────────────────────┘
                       │ HTTP
                       ▼
┌─────────────────────────────────────────────────────────┐
│                   FastAPI Backend                        │
│                      :8000                               │
│  ┌─────────────────┬──────────────┬────────────────┐   │
│  │  Chat Routes   │  Conv Routes  │  RAG Routes    │   │
│  └────────┬────────┴───────┬──────┴────────┬───────┘   │
│           │                │               │            │
│  ┌────────▼──────────────────▼──────┬──────▼──────────┐ │
│  │  LLM Inference Service           │  RAG Pipeline   │ │
│  │  (streaming + non-streaming)     │  (embeddings)   │ │
│  └────────┬────────────────┬────────┴──────┬──────────┘ │
│           │                │               │            │
│  ┌────────▼────┐ ┌─────────▼────────┐ ┌──▼────────────┐│
│  │  Ollama     │ │  PostgreSQL      │ │  Qdrant       ││
│  │  :11434     │ │  :5432           │ │  :6333        ││
│  └─────────────┘ └──────────────────┘ └───────────────┘│
│                                                          │
│  OpenTelemetry Instrumentation                          │
│  └─► OTLP Exporter :4318 (otel-collector)             │
└──────────────────────────────────────────────────────────┘

Observability Stack:
├─ OpenTelemetry Collector
├─ Prometheus :9090
├─ Grafana :3000
├─ Tempo (trace backend)
└─ Loki (log aggregation)
```

---

## Directory Structure & Component Details

### Backend (`/backend/app/`)

#### **1. Core Modules**

##### `core/settings.py`
- Centralized configuration management using Pydantic BaseSettings
- Loads environment variables from `.env` file
- Key settings:
  - `OLLAMA_BASE_URL`: Default "http://ollama:11434"
  - `DEFAULT_MODEL`: "qwen2.5-coder:7b"
  - `DEBUG`: Boolean flag for debug mode

##### `core/dependencies.py`
- Database dependency injection
- `get_db()`: Async context manager that yields PostgreSQL sessions
- Used in route handlers via FastAPI's `Depends()` mechanism

##### `main.py` (FastAPI Application Entry Point)
- Lifespan context manager for startup/shutdown
- CORS middleware configured for localhost:3000
- Telemetry setup during app initialization
- Database table creation on startup
- Route registration:
  - `/chat` - Chat endpoints
  - `/conversations` - Conversation history
  - `/rag` - RAG operations
  - `/metrics` - Prometheus metrics endpoint
  - `/` - Health check

#### **2. Database Layer**

##### `db/database.py`
- AsyncIO-compatible PostgreSQL engine setup
- Uses SQLAlchemy async driver (asyncpg)
- Connection: `postgresql+asyncpg://ai_user:ai_password@postgres:5432/ai_platform`
- Declarative Base for ORM models

##### `db/models.py`
- **Conversation Model:**
  - `id`: Primary key (Integer)
  - `title`: Optional conversation title
  - `created_at`: Timestamp
  - Relationship: One-to-many with Messages
  
- **Message Model:**
  - `id`: Primary key
  - `conversation_id`: Foreign key to Conversation
  - `role`: "user" or "assistant"
  - `content`: Text message
  - `created_at`: Timestamp
  - Relationship: Many-to-one with Conversation

#### **3. LLM Integration**

##### `llm/providers/ollama_provider.py`
- `OllamaProvider` class wraps Ollama API calls
- `generate()` method:
  - Accepts: messages list, model name, stream flag
  - Sends POST to `{OLLAMA_BASE_URL}/api/chat`
  - Returns: Assistant message content
  - Timeout: 300 seconds

##### `llm/inference.py`
- `LLMInferenceService` facade
- Methods:
  - `generate_response()`: Non-streaming inference
  - `stream_response()`: Generator for streaming tokens
  - Uses OllamaProvider internally
- Streaming yields tokens line-by-line from JSON responses

#### **4. API Routes**

##### `routes/chat.py`
- **POST `/chat`** - Non-streaming chat endpoint
  - Accepts: `ChatRequest` (conversation_id, messages, model)
  - Process:
    1. Create or fetch conversation
    2. Store user message in PostgreSQL
    3. Build full conversation history from DB
    4. Send to Ollama with system prompt
    5. Store assistant response in DB
  - Returns: `ChatResponse` with conversation_id, response, latency, token count
  - OpenTelemetry spans:
    - `chat-request` (parent)
    - `db.create_conversation`
    - `db.insert_user_message`
    - `db.fetch_conversation_history`
    - `llm.inference`
    - `db.store_assistant_message`

- **POST `/chat/stream`** - Streaming chat endpoint
  - Returns: Server-Sent Events (SSE) stream
  - Each event: `data: {"token": "...", "conversation_id": ...}`
  - Client reads stream and updates UI in real-time

##### `routes/conversations.py`
- **GET `/conversations/`** - List all conversations
  - Returns: Array of {id, created_at}
  - Ordered by creation descending (newest first)

- **GET `/conversations/{conversation_id}`** - Get conversation messages
  - Returns: Array of Message objects with role and content

#### **5. Services**

##### `services/conversation_service.py`
- **Methods:**
  - `create_conversation()`: Creates new Conversation record
  - `add_message()`: Adds Message to conversation
  - `get_messages()`: Retrieves all messages for a conversation (ordered by creation)
  - `get_all_conversations()`: Returns list of all conversations with metadata
  - `get_conversation_messages()`: Returns formatted message list

##### `services/ollama_client.py`
- Direct Ollama API wrapper
- Simple `ask_llm(prompt)` function
- Calls `POST http://ollama:11434/api/generate`
- Non-streaming responses only

#### **6. RAG (Retrieval-Augmented Generation) Pipeline**

##### `rag/ingestion/pdf_ingestor.py`
- `extract_pdf_text(file_path)`: Extracts text from PDF
- Uses PyPDF library
- Concatenates all page text with newlines

##### `rag/ingestion/chunker.py`
- `chunk_text(text, chunk_size=500)`: Splits text into overlapping/sequential chunks
- Default chunk size: 500 characters
- Returns: List of text chunks

##### `rag/embeddings/embedder.py`
- `generate_embedding(text)`: Creates semantic embeddings
- Uses Ollama embedding model: "nomic-embed-text"
- POST to `http://ollama:11434/api/embeddings`
- Returns: 768-dimensional embedding vector

##### `rag/retrieval/vector_store.py`
- Qdrant client for vector similarity search
- **Functions:**
  - `create_collection()`: Creates "documents" collection with COSINE distance
  - `store_chunks()`: Stores chunks with embeddings as points in Qdrant
  - `search_similar_chunks()`: Semantic search, returns top 3 similar chunks
- Collection config:
  - Name: "documents"
  - Vector size: 768 dimensions
  - Distance metric: COSINE similarity

##### `rag/llm/generator.py`
- `build_prompt()`: Constructs RAG prompt template
- `ask_openai()`: Uses OpenAI GPT-4 (if API key configured)
- `ask_ollama()`: Uses local Ollama model
- `ask_llm()`: Router that selects provider based on env var

##### `api/routes/rag.py`
- **POST `/rag/upload`** - PDF upload & ingestion
  - Process:
    1. Save uploaded PDF
    2. Extract text via pdf_ingestor
    3. Split into chunks via chunker
    4. Generate embeddings for each chunk
    5. Create Qdrant collection if missing
    6. Store chunks with embeddings
  - Returns: {status, chunk count}

- **POST `/rag/query`** - RAG query endpoint
  - Input: QueryRequest {query, conversation_id, provider, model}
  - Process:
    1. Generate embedding for query
    2. Search Qdrant for similar chunks (top 3)
    3. Build context from results
    4. Call LLM with context + query
  - Returns: {query, context (chunks), answer}

#### **7. Data Models (Pydantic)**

##### `models/chat.py`
- `ChatMessage`: {role: str, content: str}
- `ChatRequest`: {conversation_id?, messages[], model?, stream?}
- `ChatResponse`: {conversation_id, response, latency, tokens, model}

##### `models/conversation.py`
- `ConversationResponse`: {id, created_at, messages[]}
- `MessageResponse`: {id, role, content, created_at}

#### **8. Observability & Telemetry**

##### `observability/telemetry.py`
- OpenTelemetry setup function: `setup_telemetry(app)`
- Creates Resource with service.name="ai-backend"
- Initializes TracerProvider
- Configures OTLPSpanExporter (sends to otel-collector:4318)
- Adds BatchSpanProcessor for batching spans
- FastAPI automatic instrumentation via FastAPIInstrumentor

##### `observability/otel.py`
- Singleton tracer instance: `tracer = trace.get_tracer(__name__)`

##### `observability/logger.py`
- Structured JSON logging
- `log_event(event_name, data)`: Logs with context

##### `observability/metrics.py`
- Prometheus metrics
- `count_tokens()`: Records token counts
- Custom metrics registration

---

### Frontend (`/frontend/src/`)

#### **Main Component: `ModernAIChatUI.jsx`**

**State Management (React Hooks):**
```javascript
- messages: Array of {role: "user"|"assistant", content: string}
- conversations: Array of previous conversation summaries
- activeConversationId: Current conversation ID or null
- input: Current textarea input
- loading: Boolean flag for API call in progress
```

**Key Functions:**

1. **useEffect** - On mount
   - Calls `fetchConversations()` to load previous chats

2. **fetchConversations()**
   - GET `http://localhost:8000/conversations/`
   - Loads last 10 conversations
   - Updates sidebar conversation list

3. **loadConversation(conversationId)**
   - GET `http://localhost:8000/conversations/{id}`
   - Loads all messages from specific conversation
   - Sets as active conversation

4. **startNewChat()**
   - Clears activeConversationId
   - Resets messages to welcome message
   - Prepares for new conversation

5. **sendMessage()** - MAIN MESSAGE HANDLER
   - Pre-checks: input not empty, not already loading
   - Immediate UI update with user message
   - API call to `POST http://localhost:8000/chat`
   - Sends: {conversation_id, model: "qwen2.5-coder:7b", messages}
   - Receives: {conversation_id, response, latency, tokens, model}
   - Creates assistant message from response
   - If new conversation, saves conversation_id
   - Updates conversation list

6. **handleKeyDown()**
   - Detects Enter key without Shift
   - Triggers sendMessage()

**UI Layout:**
- **Sidebar (left, 20% width):**
  - Logo + branding
  - "New Chat" button
  - Conversation history list
  - Clickable conversation items load previous chats

- **Main Chat Area (right, 80%):**
  - Messages container with scrolling
  - Message bubbles (user = right aligned, assistant = left aligned)
  - Markdown rendering for assistant responses
  - Input textarea at bottom
  - Send button with loading state

**Styling:**
- Dark theme: black background, zinc-950 sidebar
- TailwindCSS utility classes
- React Markdown with GFM (GitHub Flavored Markdown) support
- Responsive hover/active states on buttons

---

### Configuration Files

#### **`docker-compose.yml`**
Services:
- **ollama** - Local LLM engine (port 11434)
  - GPU support via nvidia-docker
  - Persistent storage: ./data/ollama
  - Keep-alive: -1 (never unload model)

- **backend** - FastAPI server (port 8000)
  - Depends on: ollama
  - Loads .env file

- **frontend** - React dev server (port 3000)
  - Depends on: backend

- **postgres** - Database (port 5432)
  - Database: ai_platform
  - User: ai_user
  - Persistent volume: postgres_data

- **qdrant** - Vector database (port 6333)
  - Persistent storage for vectors

- **trivy** - Security scanner
  - Scans Docker images for vulnerabilities

- **security-exporter** - Vulnerability metrics (port 9110)

- **load-tester** - Load testing (profile: loadtest)

- **observability stack**:
  - otel-collector
  - prometheus (port 9090)
  - grafana (port 3000)
  - tempo (traces)

#### **`backend/requirements.txt`**
Key dependencies:
- **Web Framework:** fastapi, uvicorn
- **Async DB:** sqlalchemy, asyncpg, psycopg2-binary, alembic
- **LLM:** openai (for OpenAI fallback)
- **Vector DB:** qdrant-client
- **PDF Processing:** pypdf
- **Environment:** python-dotenv
- **Observability:** opentelemetry-api/sdk, opentelemetry-exporter-otlp, opentelemetry-instrumentation-*
- **Monitoring:** prometheus_client
- **Configuration:** pydantic-settings
- **Utilities:** requests, python-multipart

#### **`frontend/package.json`**
- **React 18.2** - UI framework
- **react-markdown** - Markdown rendering
- **remark-gfm** - GitHub Flavored Markdown support
- **TailwindCSS** - Styling
- **react-scripts** - Build tools

---

## Data Flow Diagrams

### Chat Message Flow (Non-Streaming)
```
Frontend (React)
    │
    ├─ User types message, presses Enter/Send
    │
    └─► POST /chat
        {
          conversation_id: null|int,
          messages: [{role: "user", content: "..."}],
          model: "qwen2.5-coder:7b"
        }
        │
        ▼
Backend (FastAPI)
    │
    ├─ Create conversation if new
    │  └─► INSERT INTO conversations
    │
    ├─ Store user message
    │  └─► INSERT INTO messages (role='user')
    │
    ├─ Fetch full conversation history
    │  └─► SELECT * FROM messages WHERE conversation_id=X
    │
    ├─ Call Ollama with context
    │  ├─ Send system prompt + full history
    │  └─► POST /api/chat to Ollama
    │      ├─ model: "qwen2.5-coder:7b"
    │      └─ messages: [{role: "system", ...}, {role: "user", ...}, ...]
    │
    ├─ Store assistant response
    │  └─► INSERT INTO messages (role='assistant')
    │
    └─► Return Response
        {
          conversation_id: int,
          response: "...",
          latency: 0.45s,
          tokens: 128,
          model: "qwen2.5-coder:7b"
        }
        │
        ▼
Frontend (React)
    │
    ├─ Save conversation_id
    ├─ Update messages state
    ├─ Refresh conversation list
    └─ Render assistant message
```

### RAG Query Flow
```
Frontend: User uploads PDF
    │
    └─► POST /rag/upload (multipart/form-data)
        │
        ▼
Backend RAG Pipeline:
    │
    ├─ PDF Ingestion
    │  └─ extract_pdf_text()
    │     └─ Read PDF → Extract text from all pages
    │
    ├─ Text Chunking
    │  └─ chunk_text(text, chunk_size=500)
    │     └─ Split into ~500 char chunks
    │
    ├─ Embedding Generation
    │  └─ For each chunk:
    │     └─ generate_embedding(chunk)
    │        └─ POST to Ollama /api/embeddings
    │           └─ model: "nomic-embed-text"
    │           └─ Returns: 768-dim vector
    │
    ├─ Vector Storage
    │  └─ store_chunks(chunks, embeddings)
    │     └─ Qdrant upsert
    │        └─ Create collection if missing
    │        └─ Store points with text payload
    │
    └─► Return {status: "success", chunks: N}

Later, User queries:
    │
    └─► POST /rag/query
        {query: "...", conversation_id: ..., provider: "ollama"}
        │
        ▼
Backend RAG:
    │
    ├─ Generate query embedding
    │  └─ generate_embedding(query)
    │
    ├─ Search Qdrant
    │  └─ search_similar_chunks(embedding, limit=3)
    │     └─ Return top 3 semantically similar chunks
    │
    ├─ Build context
    │  └─ Concatenate retrieved chunks
    │
    ├─ Generate answer
    │  └─ ask_llm(query, context)
    │     └─ Build RAG prompt
    │     └─ Call Ollama or OpenAI
    │
    └─► Return {query, context: [chunks], answer}
```

### Observability Flow
```
Backend Operations
    │
    ├─ Create OTEL Spans
    │  ├─ chat-request (parent)
    │  ├─ db.create_conversation
    │  ├─ db.insert_user_message
    │  ├─ db.fetch_conversation_history
    │  ├─ llm.inference
    │  └─ db.store_assistant_message
    │
├─ Emit Metrics
│  ├─ token_count (counter)
│  ├─ request_latency (histogram)
│  └─ active_conversations (gauge)
│
├─ Structured Logs
│  └─ request_received, inference_complete, etc.
│
└─► OTLP Exporter
    │
    └─► http://otel-collector:4318/v1/traces
        │
        ├─► Tempo (trace backend)
        │   └─ Queryable in Grafana
        │
        ├─► Prometheus (via custom exporters)
        │   └─ Dashboards in Grafana
        │
        └─► Loki (logs)
            └─ Log aggregation
```

---

## Key Workflows

### Workflow 1: New User Chat
1. User opens frontend
2. `fetchConversations()` loads previous conversations
3. User types message
4. `sendMessage()` is triggered
5. User message added to UI immediately
6. Backend creates new Conversation record
7. Backend stores Message record with role="user"
8. Backend fetches conversation history (just the one message)
9. Backend sends to Ollama with system prompt
10. Ollama generates response
11. Backend stores Message record with role="assistant"
12. Response returned to frontend
13. Frontend saves conversation_id
14. Frontend renders response
15. Frontend refreshes conversation list

### Workflow 2: Continue Existing Conversation
1. User clicks conversation in sidebar
2. `loadConversation(id)` fetches all messages
3. UI updates with history
4. User types new message
5. `sendMessage()` sends to backend with conversation_id
6. Backend fetches full conversation history (all previous messages)
7. Backend builds context with ALL messages (system prompt + full history)
8. Ollama generates response based on context
9. Response stored and returned
10. Frontend appends assistant message to existing conversation

### Workflow 3: Document Upload & RAG Query
1. User uploads PDF via `/rag/upload`
2. Backend extracts text (pypdf)
3. Backend chunks text (500 char chunks)
4. Backend generates embeddings for each chunk (Ollama)
5. Backend stores chunks in Qdrant vector DB
6. User queries via `/rag/query`
7. Backend embeds query
8. Backend searches Qdrant (top 3 similar)
9. Backend calls Ollama with retrieved context
10. Response returned with citations

---

## Important Implementation Details

### Conversation Context Handling
- Backend always fetches FULL conversation history from PostgreSQL
- All previous messages are included in the Ollama API call
- This enables coherent multi-turn conversations
- System prompt is prepended to the full history

### Streaming Architecture
- Frontend can switch between streaming and non-streaming modes
- Non-streaming: Wait for full response, then display
- Streaming: Receive tokens via SSE, update UI incrementally
- Both use the same underlying Ollama `/api/chat` endpoint

### Database Schema
- Normalized design with separate Conversations and Messages tables
- Cascade delete: Deleting conversation removes all messages
- Timestamps track when messages were created
- Supports multiple conversations per session

### Vector Store (Qdrant)
- Separate from conversation database
- Used only for RAG document retrieval
- Independent of chat history
- Supports multiple document collections (could be extended)

### Observability Instrumentation
- FastAPI automatically instrumented via `FastAPIInstrumentor`
- Custom spans for business logic (db operations, LLM calls)
- Metrics exported to Prometheus
- Traces exported to Tempo
- Logs structured and exportable

### Error Handling
- Frontend catches fetch errors, shows "Failed to connect" message
- Backend returns 500 errors on exceptions
- Ollama timeouts set to 300 seconds
- Database errors propagate through FastAPI exception handlers

### Security Considerations
- CORS restricted to localhost:3000
- Database credentials in .env (not in code)
- API keys (OpenAI) in .env
- Ollama running on internal network
- Qdrant not exposed directly to frontend
- Trivy scans for container vulnerabilities

---

## Configuration & Environment Variables

### Required Environment Variables (.env)
```env
# Ollama
OLLAMA_BASE_URL=http://ollama:11434
OLLAMA_MODEL=qwen2.5-coder:7b

# Database
DATABASE_URL=postgresql+asyncpg://ai_user:ai_password@postgres:5432/ai_platform

# Optional: OpenAI fallback
OPENAI_API_KEY=sk-...

# Model Provider (ollama or openai)
MODEL_PROVIDER=ollama

# Observability
OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector:4318
```

### Port Mappings
- Frontend: :3000
- Backend: :8000
- Ollama: :11434
- PostgreSQL: :5432
- Qdrant: :6333
- Prometheus: :9090
- Grafana: :3000 (same as frontend, typically run on different port)

---

## Testing & Performance

### Load Testing
- Load test harness in `/load-test/` directory
- Can be run with `docker compose --profile loadtest up`
- Uses Apache Bench or custom Node.js script
- Tests chat endpoints under load

### Monitoring
- Prometheus scrapes metrics from `:8000/metrics` every 5 seconds
- Grafana dashboards available in `/observability/dashboards/`
- Key metrics:
  - HTTP request latency
  - Token counts
  - Database query times
  - Error rates

---

## Deployment Notes

### Docker Compose Services
- All services configured in single docker-compose.yml
- GPU support via nvidia-docker for Ollama
- PostgreSQL persistent volume
- Ollama model cache persistent

### Model Management
- Default model: qwen2.5-coder:7b (7B parameter Qwen model optimized for coding)
- Embedding model: nomic-embed-text (768 dimensions)
- Models pulled from Ollama registry on first run
- Kept in memory indefinitely (`OLLAMA_KEEP_ALIVE=-1`)

### Performance Tuning
- Database connection pooling via SQLAlchemy
- Batch span processing for telemetry
- Prometheus scrape interval: 5 seconds
- OTLP batch export (configurable)

---

## Known Limitations & Future Enhancements

### Current Limitations
- No user authentication
- No rate limiting
- No request validation/sanitization
- RAG: Simple linear chunking (no overlap)
- RAG: No document versioning
- No support for image uploads
- Single model at a time

### Possible Enhancements
- User authentication & authorization
- Fine-tuning of local models
- Multiple model support with switching
- Advanced RAG: hierarchical chunking, metadata filtering
- Conversation export/import
- Custom system prompts
- Plugin system for tools/APIs
- Real-time collaboration
- Voice input/output
- Image generation capability

---

## Troubleshooting

### Common Issues

**Backend won't connect to Ollama:**
- Check Ollama container is running: `docker ps`
- Verify OLLAMA_BASE_URL matches container hostname
- Check network configuration: `docker network ls`

**Database connection errors:**
- Ensure PostgreSQL container running
- Check DATABASE_URL format
- Verify credentials match docker-compose.yml

**Vectors not being stored:**
- Ensure Qdrant container running
- Check collection was created
- Verify embedding model (nomic-embed-text) is pulled

**Frontend not connecting to backend:**
- Check CORS configuration in main.py
- Verify backend is running on :8000
- Check browser console for errors

**Observability not working:**
- Ensure otel-collector running
- Check OTEL_EXPORTER_OTLP_ENDPOINT
- Verify traces endpoint is :4318

---

## Code Quality & Standards

- Type hints used throughout Python code
- Pydantic models for request/response validation
- Async/await for all I/O operations
- React functional components with hooks
- TailwindCSS for styling consistency
- OpenTelemetry for observability best practices
- Docker best practices (multi-stage builds possible)

---

## Entry Points

### Backend
- **Main:** `backend/app/main.py`
- **Run:** `uvicorn app.main:app --reload` (dev) or `uvicorn app.main:app` (prod)

### Frontend
- **Main:** `frontend/src/App.js`
- **Run:** `npm start`

### Docker
- **Build & Run:** `docker compose up --build`

---

## Summary

This is a full-featured local AI platform with:
1. **Chat Interface** - Real-time messaging with conversation history
2. **LLM Integration** - Local Ollama with qwen2.5-coder:7b
3. **RAG Capability** - PDF ingestion and semantic search
4. **Database** - PostgreSQL for structured data
5. **Vector Store** - Qdrant for semantic similarity
6. **Observability** - Full OpenTelemetry tracing and metrics
7. **Security** - Container scanning and audit logging
8. **Scalability** - Async/await patterns and connection pooling
9. **Modern Stack** - React, FastAPI, Docker, TailwindCSS

The application demonstrates enterprise-grade patterns for AI applications including proper observability, database management, and clean architecture principles.

