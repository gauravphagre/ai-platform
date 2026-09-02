"""
# Workflow Architecture Documentation

## Overview

The `workflows/` module implements **LangGraph-based deterministic workflows** for incident response, task orchestration, and agent coordination.

**Key Design Principles:**
- ✅ All state is Pydantic-serializable (for checkpointing)
- ✅ Async/await throughout (non-blocking)
- ✅ Integrated with central `LLMService` (no direct provider calls)
- ✅ Observable via structured logging
- ✅ Pause/resume capability (checkpoint-enabled)
- ✅ Auto-routing based on incident severity/confidence

---

## Directory Structure

```
workflows/
├── __init__.py                          (Module exports)
│
├── incident_response/                   (Incident automation workflow)
│   ├── __init__.py
│   ├── state.py                         (Pydantic state models)
│   ├── graph.py                         (LangGraph workflow definition)
│   ├── router.py                        (Routing logic: auto-execute vs human review)
│   │
│   └── nodes/
│       ├── __init__.py
│       ├── retrieve_logs.py             (Fetch logs from observability)
│       ├── retrieve_metrics.py          (Fetch metrics from monitoring)
│       ├── analyze_root_cause.py        (LLM-powered analysis)
│       └── suggest_remediation.py       (LLM-powered recommendations)
│
└── common/
    ├── __init__.py
    ├── base_state.py                    (Abstract base for all states)
    └── workflow_utils.py                (Shared utilities)
```

---

## Incident Response Workflow

### State Model (`incident_response/state.py`)

The `IncidentState` is a Pydantic model that tracks the full lifecycle of an incident:

```python
IncidentState(
    # Input
    incident_id: str,
    incident_description: str,
    severity: "critical" | "high" | "medium" | "low",
    
    # Collected Data (populated by nodes)
    logs: list[LogEntry],
    metrics: list[Metric],
    
    # Analysis (populated by LLM)
    root_cause: RootCauseAnalysis,
    
    # Remediation (auto-populated)
    remediation_actions: list[RemediationAction],
    selected_action: RemediationAction,
    
    # Execution
    executed: bool,
    execution_status: str | None,
    execution_error: str | None,
    
    # Metadata
    created_at: str,
    updated_at: str,
    workflow_run_id: str,
)
```

### Workflow Graph (`incident_response/graph.py`)

The workflow follows this DAG:

```
                    START
                    ↙   ↘
            retrieve_logs  retrieve_metrics
                    ↘   ↙
            analyze_root_cause
                    ↓
            suggest_remediation
                    ↓
                   END
```

**Step 1: Retrieve Logs**
- Queries observability system (Tempo, Loki)
- Filters by time window, severity
- Returns list of `LogEntry` objects

**Step 2: Retrieve Metrics**
- Queries monitoring system (Prometheus, Datadog)
- Filters by service, instance
- Returns list of `Metric` objects

**Step 3: Analyze Root Cause**
- Calls `LLMService.generate_response()` with logs + metrics
- LLM synthesizes data → root cause hypothesis
- Returns `RootCauseAnalysis` with confidence score

**Step 4: Suggest Remediation**
- Calls `LLMService.generate_response()` with root cause
- LLM generates prioritized remediation actions
- Auto-selects highest-priority action
- Returns list of `RemediationAction` objects

### Routing (`incident_response/router.py`)

After the workflow completes, the `route_incident()` function determines handling:

```python
route = route_incident(state)
# Returns: "auto_execute" | "human_review" | "quarantine"
```

**Routing Logic:**

| Condition | Route | Reason |
|-----------|-------|--------|
| `confidence < 0.5` | `quarantine` | Uncertain root cause → alert humans |
| `severity="low" & confidence >= 0.8` | `auto_execute` | Low risk + high confidence → auto-remediate |
| `severity in ["medium", "high", "critical"]` | `human_review` | High severity → require approval |
| Default | `human_review` | Safe default |

---

## Common Utilities (`common/`)

### Base State (`base_state.py`)

All workflow states inherit from `BaseWorkflowState`:

```python
class BaseWorkflowState(BaseModel):
    workflow_type: str          # e.g., "incident_response"
    workflow_run_id: str        # UUID for this run
    created_at: str             # ISO timestamp
    updated_at: str             # ISO timestamp
    checkpoint: str             # Current node name
    status: str                 # "running", "completed", "failed", "paused"
    error: str | None           # Error message if failed
    metadata: dict              # Arbitrary context
```

**Helper Methods:**
- `.mark_complete()` - Mark as done
- `.mark_failed(error)` - Mark as failed with message
- `.mark_paused()` - Pause for human review
- `.to_dict()` - Serialize for checkpoint
- `.from_dict(data)` - Deserialize from checkpoint

### Utilities (`workflow_utils.py`)

**Key Functions:**
- `state_to_dict(state)` - Serialize state for storage
- `dict_to_state(data, StateClass)` - Deserialize from storage
- `log_node_transition(workflow_id, from_node, to_node, state)` - Observe node transitions
- `validate_state_transition(state, valid_statuses)` - Enforce valid transitions
- `merge_state_updates(state, updates)` - Safely apply updates (immutable fields protected)

---

## API Endpoints (`api/workflows/workflows.py`)

### Create Incident Workflow

**POST /api/workflows/incidents/create**

Request:
```json
{
  "incident_description": "High error rate in auth service",
  "severity": "critical"
}
```

Response:
```json
{
  "incident_id": "INC-A1B2C3D4",
  "workflow_id": "uuid-here",
  "status": "completed",
  "route": "human_review",
  "root_cause": {
    "hypothesis": "Database connection pool exhausted",
    "confidence": 0.92,
    "affected_services": ["auth-service", "api-gateway"],
    "contributing_factors": ["spike in login requests", "slow DB queries"]
  },
  "remediation_actions": [
    {
      "action": "Increase connection pool size to 20",
      "priority": 1,
      "estimated_duration_seconds": 60,
      "rollback_plan": "Revert ConfigMap"
    }
  ],
  "selected_action": { ... }
}
```

### Get Workflow Status

**GET /api/workflows/incidents/{workflow_id}**

Returns current state, analysis, and remediation options.

### Approve Remediation

**POST /api/workflows/incidents/{workflow_id}/approve**

Request:
```json
{
  "action_index": 0
}
```

Executes the selected remediation action.

---

## Integration with LLMService

All LLM calls go through the central `LLMService`:

```python
from app.llm.schemas import ChatMessage, GenerateRequest
from app.llm.service import LLMService

llm_service = LLMService()

request = GenerateRequest(
    messages=[
        ChatMessage(role="system", content="..."),
        ChatMessage(role="user", content="..."),
    ],
    model="qwen2.5-coder:7b",
    stream=False,
)

response = await llm_service.generate_response(request)
print(response.content)  # str
```

**This ensures:**
- Single entry point for LLM access
- Consistent error handling
- Observable via traces/metrics
- Easy to swap providers (Ollama ↔ OpenAI)

---

## Testing the Workflow

### Run Locally

```python
from app.workflows.incident_response import (
    build_incident_workflow,
    IncidentState,
)
from datetime import datetime
import asyncio

async def test_workflow():
    state = IncidentState(
        incident_id="TEST-001",
        incident_description="Test incident",
        severity="medium",
        created_at=datetime.utcnow().isoformat(),
        updated_at=datetime.utcnow().isoformat(),
    )
    
    workflow = build_incident_workflow()
    output = workflow.invoke(state)
    
    print(f"Root cause: {output.root_cause}")
    print(f"Remediation: {output.remediation_actions}")

asyncio.run(test_workflow())
```

### Via API

```bash
curl -X POST http://localhost:8000/api/workflows/incidents/create \
  -H "Content-Type: application/json" \
  -d '{
    "incident_description": "High latency detected",
    "severity": "high"
  }'
```

---

## Future Extensions

### 1. **Execution Node**
Add automatic remediation execution for low-severity incidents:
```python
workflow.add_node("execute_remediation", execute_remediation)
workflow.add_conditional_edges(
    "suggest_remediation",
    route_incident,
    {
        "auto_execute": "execute_remediation",
        "human_review": END,
        "quarantine": END,
    }
)
```

### 2. **Escalation Workflow**
Route critical incidents to on-call engineer:
```python
workflow.add_node("escalate_to_oncall", escalate_to_oncall)
```

### 3. **Feedback Loop**
Learn from past incidents:
```python
workflow.add_edge("execute_remediation", "collect_feedback")
workflow.add_node("collect_feedback", collect_feedback)
```

### 4. **Multi-Incident Aggregation**
Correlate related incidents across services.

### 5. **Predictive Incident Prevention**
Use metrics to predict incidents before they happen.

---

## Monitoring & Observability

All workflow transitions are logged:

```
workflow_transition: incident_response | retrieve_logs → retrieve_metrics
workflow_transition: incident_response | analyze_root_cause
incident_analyzed: INC-A1B2C3D4 | confidence=0.92 | route=human_review
remediation_approved: INC-A1B2C3D4 | action="increase pool"
```

Accessible via:
- **Logs:** Loki/CloudWatch
- **Traces:** Tempo/Jaeger (OpenTelemetry)
- **Metrics:** Prometheus

---

## References

- **LangGraph:** https://github.com/langchain-ai/langgraph
- **Pydantic:** https://docs.pydantic.dev/
- **LLMService:** `app/llm/service.py`
- **BaseState:** `app/workflows/common/base_state.py`
"""

