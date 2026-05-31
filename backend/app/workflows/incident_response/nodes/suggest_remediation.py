"""
Suggest Remediation Node

LLM-powered remediation suggestion using root cause analysis.

Uses LLMService to:
1. Generate prioritized list of remediation actions
2. Estimate action duration
3. Outline rollback plans
4. Identify prerequisites
"""

from app.llm.schemas import ChatMessage, GenerateRequest
from app.llm.service import LLMService
from app.workflows.incident_response.state import IncidentState, RemediationAction
import json


async def suggest_remediation(state: IncidentState) -> IncidentState:
    """
    Suggest remediation actions based on root cause analysis.

    Calls LLMService to generate a prioritized list of remediation
    actions with estimated duration and rollback plans.

    Args:
        state: Current incident state (should have root_cause)

    Returns:
        IncidentState: State with remediation_actions populated
    """

    if not state.root_cause:
        return state

    # ==================== BUILD CONTEXT ====================
    context = f"""
Incident Root Cause Analysis:

Hypothesis: {state.root_cause.hypothesis}
Confidence: {state.root_cause.confidence:.1%}
Affected Services: {', '.join(state.root_cause.affected_services)}
Contributing Factors:
{chr(10).join(f'  - {factor}' for factor in state.root_cause.contributing_factors)}

Based on this analysis, suggest 3-5 remediation actions in priority order.

For each action, provide:
- action (specific command or procedure)
- priority (1=critical/highest to 5=lowest)
- estimated_duration_seconds
- rollback_plan (if applicable)
- prerequisites (list of required conditions)

Return as JSON array of objects, no additional text.

Example format:
[
  {{
    "action": "Increase database connection pool size from 10 to 20",
    "priority": 1,
    "estimated_duration_seconds": 60,
    "rollback_plan": "Revert pool size via ConfigMap update",
    "prerequisites": ["database-service must be running"]
  }}
]
"""

    # ==================== CALL LLM ====================
    llm_service = LLMService()

    llm_request = GenerateRequest(
        messages=[
            ChatMessage(
                role="system",
                content=(
                    "You are an expert SRE/DevOps engineer. "
                    "Based on the root cause analysis, suggest concrete remediation actions. "
                    "Be specific and practical. Return JSON array only, no markdown or extra text."
                ),
            ),
            ChatMessage(role="user", content=context),
        ],
        model="qwen2.5-coder:7b",
        stream=False,
    )

    try:
        llm_response = await llm_service.generate_response(llm_request)
        remediation_text = llm_response.content

        # Parse JSON from response
        actions_json = json.loads(remediation_text)

        state.remediation_actions = [
            RemediationAction(
                action=action.get("action", ""),
                priority=int(action.get("priority", 3)),
                estimated_duration_seconds=int(action.get("estimated_duration_seconds", 300)),
                rollback_plan=action.get("rollback_plan"),
                prerequisites=action.get("prerequisites", []),
            )
            for action in actions_json
        ]
    except Exception as e:
        # If LLM call fails, populate with generic remediation
        state.remediation_actions = [
            RemediationAction(
                action="Manual investigation required",
                priority=1,
                estimated_duration_seconds=600,
                rollback_plan=None,
                prerequisites=[],
            ),
        ]

    # Auto-select highest-priority action
    if state.remediation_actions:
        state.selected_action = sorted(
            state.remediation_actions,
            key=lambda a: a.priority
        )[0]

    return state

