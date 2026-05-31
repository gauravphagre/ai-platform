"""
Workflows API Endpoints

HTTP endpoints for workflow execution and management.

Endpoints:
- POST /workflows/incidents/create: Create and run incident workflow
- GET /workflows/incidents/{id}: Get incident workflow status
- POST /workflows/incidents/{id}/approve: Approve remediation action
- GET /workflows/incidents/{id}/history: Get workflow event history
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import uuid4
from datetime import datetime, UTC

from app.workflows.incident_response import (
    IncidentState,
    build_incident_workflow,
    route_incident,
)
from app.core.dependencies import get_db
from app.observability.logger import log_event
from app.repositories.workflow_run_repository import WorkflowRunRepository

router = APIRouter(prefix="/workflows", tags=["workflows"])


class IncidentRequest(BaseModel):
    """Request to create an incident workflow."""
    incident_description: str
    severity: str  # "critical", "high", "medium", "low"


class RemediationApprovalRequest(BaseModel):
    """Request to approve a remediation action."""
    action_index: int = 0  # Which remediation action to execute


@router.post("/incidents/create")
async def create_incident_workflow(
    request: IncidentRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Create and execute an incident response workflow.

    Runs the full incident workflow:
    1. Retrieve logs and metrics
    2. Analyze root cause
    3. Suggest remediation

    Returns workflow ID for polling.
    """

    incident_id = f"INC-{uuid4().hex[:8].upper()}"
    workflow_run_id = str(uuid4())

    log_event(
        "incident_created",
        {
            "incident_id": incident_id,
            "severity": request.severity,
            "description": request.incident_description,
        }
    )

    state = IncidentState(
        incident_id=incident_id,
        incident_description=request.incident_description,
        severity=request.severity,
        created_at=datetime.now(UTC).isoformat(),
        updated_at=datetime.now(UTC).isoformat(),
        workflow_run_id=workflow_run_id,
    )

    workflow = build_incident_workflow()
    repo = WorkflowRunRepository(db)

    try:
        output_state = workflow.invoke(state)
        route = route_incident(output_state)

        await repo.create_run(
            workflow_id=workflow_run_id,
            workflow_type="incident_response",
            status="completed",
            state=output_state.model_dump(mode="json"),
        )

        log_event(
            "incident_analyzed",
            {
                "incident_id": incident_id,
                "workflow_id": workflow_run_id,
                "route": route,
                "root_cause_confidence": (
                    output_state.root_cause.confidence
                    if output_state.root_cause else 0.0
                ),
            }
        )

        return {
            "incident_id": incident_id,
            "workflow_id": workflow_run_id,
            "status": "completed",
            "route": route,
            "root_cause": (
                output_state.root_cause.model_dump()
                if output_state.root_cause else None
            ),
            "remediation_actions": [
                action.model_dump()
                for action in output_state.remediation_actions
            ],
            "selected_action": (
                output_state.selected_action.model_dump()
                if output_state.selected_action else None
            ),
        }

    except Exception as e:
        log_event(
            "incident_workflow_failed",
            {
                "incident_id": incident_id,
                "error": str(e),
            }
        )
        raise HTTPException(
            status_code=500,
            detail=f"Workflow execution failed: {str(e)}"
        )


@router.get("/incidents/{workflow_id}")
async def get_incident_workflow(
    workflow_id: str,
    db: AsyncSession = Depends(get_db),
):
    """
    Get status of an incident workflow.

    Returns the current state, analysis, and remediation options.
    """

    repo = WorkflowRunRepository(db)
    run = await repo.get_run(workflow_id)
    if not run:
        raise HTTPException(status_code=404, detail="Workflow not found")

    state = IncidentState.model_validate(run.state)

    return {
        "workflow_id": workflow_id,
        "incident_id": state.incident_id,
        "status": run.status,
        "root_cause": (
            state.root_cause.model_dump()
            if state.root_cause else None
        ),
        "remediation_actions": [
            action.model_dump()
            for action in state.remediation_actions
        ],
        "selected_action": (
            state.selected_action.model_dump()
            if state.selected_action else None
        ),
    }


@router.post("/incidents/{workflow_id}/approve")
async def approve_remediation(
    workflow_id: str,
    request: RemediationApprovalRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Approve and execute a remediation action.

    In production, this would:
    1. Validate approval permissions
    2. Execute the remediation
    3. Monitor results
    4. Auto-rollback if needed
    """

    repo = WorkflowRunRepository(db)
    run = await repo.get_run(workflow_id)
    if not run:
        raise HTTPException(status_code=404, detail="Workflow not found")

    state = IncidentState.model_validate(run.state)

    if request.action_index >= len(state.remediation_actions):
        raise HTTPException(status_code=400, detail="Invalid action index")

    action = state.remediation_actions[request.action_index]

    log_event(
        "remediation_approved",
        {
            "incident_id": state.incident_id,
            "workflow_id": workflow_id,
            "action": action.action,
            "priority": action.priority,
        }
    )

    state.executed = True
    state.execution_status = "success"
    state.selected_action = action

    await repo.update_run(
        workflow_id,
        status="completed",
        state=state.model_dump(mode="json"),
    )

    return {
        "workflow_id": workflow_id,
        "incident_id": state.incident_id,
        "action_executed": action.model_dump(),
        "status": "completed",
    }
