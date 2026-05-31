# Project Directory & File Structure

Generated: May 30, 2026 (Updated)

> Note: This structure intentionally excludes bulky/generated folders such as:
> - `.git/`
> - Python virtualenv internals under `backend/Lib`, `backend/Include`, `backend/Scripts`
> - `**/__pycache__/`
> - `frontend/node_modules/`

## Top-level

```
ai-platform/
├── .env
├── .gitignore
├── CODEBASE_DOCUMENTATION.md
├── CURRENT_DIRECTORY_STRUCTURE.md
├── DIRECTORY_STRUCTURE.md
├── RESTRUCTURE_SUMMARY.md
├── WORKFLOW_CHECKLIST.md
├── WORKFLOW_DOCUMENTATION_INDEX.md
├── WORKFLOW_IMPLEMENTATION_SUMMARY.md
├── WORKFLOW_QUICKSTART.md
├── dir_structure.md
├── directory_tree.txt
├── docker-compose.yml
├── resume.pdf
│
├── backend/
├── frontend/
├── observability/
├── ollama/
├── security/
├── load-test/
└── data/
```

## backend/

```
backend/
├── Dockerfile
├── requirements.txt
├── __init__.py
└── app/
    ├── __init__.py
    ├── main.py
    │
    ├── api/
    │   ├── chat/
    │   │   ├── __init__.py
    │   │   ├── chat.py
    │   │   └── utils.py
    │   ├── conversations/
    │   │   ├── __init__.py
    │   │   └── conversations.py
    │   ├── health/
    │   │   ├── __init__.py
    │   │   └── health.py
    │   ├── rag/
    │   │   ├── __init__.py
    │   │   └── rag.py
    │   └── workflows/
    │       ├── __init__.py
    │       └── workflows.py
    │
    ├── core/
    │   ├── dependencies.py
    │   └── settings.py
    │
    ├── config/
    │   └── __init__.py
    │
    ├── tests/
    │   └── __init__.py
    │
    ├── repositories/
    │   ├── __init__.py
    │   ├── conversation_repository.py
    │   └── workflow_run_repository.py
    │
    ├── domain/
    │   └── __init__.py
    │
    ├── infrastructure/
    │   ├── __init__.py
    │   ├── cache/
    │   │   └── __init__.py
    │   ├── messaging/
    │   │   └── __init__.py
    │   ├── storage/
    │   │   └── __init__.py
    │   ├── events/
    │   │   ├── __init__.py
    │   │   ├── event_bus.py
    │   │   ├── event_models.py
    │   │   └── publishers.py
    │   └── database/
    │       ├── __init__.py
    │       ├── database.py
    │       ├── models.py                 # compatibility re-export
    │       └── models/
    │           ├── __init__.py
    │           ├── conversation.py
    │           ├── message.py
    │           ├── incident.py
    │           └── workflow_run.py
    │
    ├── llm/
    │   ├── __init__.py
    │   ├── exceptions.py
    │   ├── interfaces.py
    │   ├── schemas.py
    │   ├── service.py
    │   ├── tokenizer.py
    │   ├── prompts/
    │   │   └── system.py
    │   └── providers/
    │       ├── base.py
    │       └── ollama_provider.py
    │
    ├── rag/
    │   ├── __init__.py
    │   ├── embeddings/
    │   │   ├── __init__.py
    │   │   └── embedder.py
    │   ├── ingestion/
    │   │   ├── __init__.py
    │   │   ├── chunker.py
    │   │   └── pdf_ingestor.py
    │   └── retrieval/
    │       ├── __init__.py
    │       └── vector_store.py
    │
    ├── agents/
    │   ├── __init__.py
    │   ├── base/
    │   │   ├── __init__.py
    │   │   ├── agent.py
    │   │   └── state.py
    │   ├── planner/
    │   │   ├── __init__.py
    │   │   └── planner_agent.py
    │   ├── remediation/
    │   │   ├── __init__.py
    │   │   └── remediation_agent.py
    │   ├── retrieval/
    │   │   ├── __init__.py
    │   │   └── retrieval_agent.py
    │   ├── summarization/
    │   │   ├── __init__.py
    │   │   └── summary_agent.py
    │   └── verification/
    │       ├── __init__.py
    │       └── verification_agent.py
    │
    ├── tools/
    │   ├── __init__.py
    │   ├── executor.py
    │   ├── registry.py
    │   ├── python_tool.py
    │   ├── docker/
    │   │   ├── __init__.py
    │   │   └── docker_tool.py
    │   ├── kubernetes/
    │   │   ├── __init__.py
    │   │   └── kubernetes_tool.py
    │   ├── prometheus/
    │   │   ├── __init__.py
    │   │   └── prometheus_tool.py
    │   ├── loki/
    │   │   ├── __init__.py
    │   │   └── loki_tool.py
    │   ├── github/
    │   │   ├── __init__.py
    │   │   └── github_tool.py
    │   ├── filesystem/
    │   │   ├── __init__.py
    │   │   └── filesystem_tool.py
    │   └── shell/
    │       ├── __init__.py
    │       └── shell_tool.py
    │
    ├── workflows/
    │   ├── __init__.py
    │   ├── registry.py
    │   ├── common/
    │   │   ├── __init__.py
    │   │   ├── base_state.py
    │   │   ├── base_workflow.py
    │   │   └── workflow_utils.py
    │   ├── incident_response/
    │   │   ├── __init__.py
    │   │   ├── graph.py
    │   │   ├── router.py
    │   │   ├── state.py
    │   │   └── nodes/
    │   │       ├── __init__.py
    │   │       ├── analyze_root_cause.py
    │   │       ├── retrieve_logs.py
    │   │       ├── retrieve_metrics.py
    │   │       └── suggest_remediation.py
    │   ├── deployment_assistant/
    │   │   └── __init__.py
    │   ├── kubernetes_troubleshooting/
    │   │   └── __init__.py
    │   ├── security_investigation/
    │   │   └── __init__.py
    │   └── cost_optimization/
    │       └── __init__.py
    │
    ├── runtime/
    │   ├── __init__.py
    │   ├── workers/
    │   │   └── worker_manager.py
    │   ├── queues/
    │   │   ├── __init__.py
    │   │   ├── redis_queue.py
    │   │   └── task_dispatcher.py
    │   └── schedulers/
    │       └── __init__.py
    │
    ├── integrations/
    │   ├── __init__.py
    │   ├── prometheus/
    │   │   ├── __init__.py
    │   │   ├── client.py
    │   │   ├── queries.py
    │   │   └── service.py
    │   ├── loki/
    │   │   ├── __init__.py
    │   │   ├── client.py
    │   │   ├── log_queries.py
    │   │   └── service.py
    │   ├── kubernetes/
    │   │   ├── __init__.py
    │   │   ├── client.py
    │   │   ├── cluster_service.py       # compatibility wrapper
    │   │   └── service.py
    │   ├── github/
    │   │   ├── __init__.py
    │   │   ├── client.py
    │   │   ├── github_service.py        # compatibility wrapper
    │   │   └── service.py
    │   └── docker/
    │       ├── __init__.py
    │       ├── client.py
    │       ├── docker_service.py        # compatibility wrapper
    │       └── service.py
    │
    ├── mcp/
    │   ├── __init__.py
    │   ├── registry/
    │   │   ├── __init__.py
    │   │   └── tool_registry.py
    │   ├── servers/
    │   │   ├── __init__.py
    │   │   └── filesystem_server.py
    │   ├── clients/
    │   │   ├── __init__.py
    │   │   └── mcp_client.py
    │   ├── permissions/
    │   │   ├── __init__.py
    │   │   └── policy_engine.py
    │   └── schemas/
    │       ├── __init__.py
    │       └── tool_schema.py
    │
    ├── evals/
    │   ├── __init__.py
    │   ├── retrieval/
    │   │   ├── __init__.py
    │   │   └── retrieval_eval.py
    │   ├── workflows/
    │   │   ├── __init__.py
    │   │   └── workflow_eval.py
    │   ├── hallucination/
    │   │   ├── __init__.py
    │   │   └── hallucination_eval.py
    │   └── tool_accuracy/
    │       ├── __init__.py
    │       └── tool_eval.py
    │
    ├── services/
    │   ├── __init__.py
    │   └── conversation_service.py
    │
    ├── schemas/
    │   ├── __init__.py
    │   ├── chat.py
    │   ├── incident.py
    │   ├── remediation.py
    │   ├── telemetry.py
    │   └── workflow.py
    │
    └── observability/
        ├── __init__.py
        ├── logger.py
        ├── metrics.py
        ├── otel.py
        └── telemetry.py
```

## frontend/

```
frontend/
├── Dockerfile
├── package.json
├── postcss.config.js
├── tailwind.config.js
├── public/
│   └── index.html
└── src/
    ├── App.css
    ├── App.js
    ├── index.css
    ├── index.js
    └── components/
```

## observability/

```
observability/
├── docker-compose.yml
├── otel-collector.yml
├── prometheus.yml
├── tempo.yaml
└── dashboards/
    ├── ai_app_obs.json
    ├── ai_logs_dashboard.json
    ├── ai_observability_dashboard.json
    └── ai_vulnerability_dashboard.json
```

## load-test/

```
load-test/
├── Dockerfile
└── load-test.js
```

## ollama/

```
ollama/
├── Dockerfile
└── start.sh
```

## security/

```
security/
├── Dockerfile
├── scan.sh
├── trivy_metrics.py
└── trivy/
    ├── metrics/
    └── reports/
```

## data/

```
data/
└── ollama/
    ├── config.json
    ├── history
    ├── id_ed25519
    ├── id_ed25519.pub
    ├── backup/
    ├── cache/
    └── models/
```
