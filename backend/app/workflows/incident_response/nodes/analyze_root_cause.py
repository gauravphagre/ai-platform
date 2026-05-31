"""
Analyze Root Cause Node

LLM-powered incident analysis using collected logs and metrics.

Uses the central LLMService to:
1. Synthesize logs + metrics into incident narrative
2. Generate root cause hypothesis
3. Score confidence
4. Identify affected services
"""

from app.llm.schemas import ChatMessage, GenerateRequest
from app.llm.service import LLMService
from app.workflows.incident_response.state import IncidentState, RootCauseAnalysis
import json


async def analyze_root_cause(state: IncidentState) -> IncidentState:
    """
    Analyze logs and metrics to determine root cause.

    Calls LLMService to synthesize collected data into a structured
    root cause analysis with confidence scoring.

    Args:
        state: Current incident state (should have logs + metrics)

    Returns:
        IncidentState: State with root_cause populated
    """

    if not state.logs or not state.metrics:
        return state

    # ==================== BUILD CONTEXT ====================
    logs_text = "\n".join([
        f"[{log.timestamp}] {log.level} {log.service}: {log.message}"
        for log in state.logs
    ])

    metrics_text = "\n".join([
        f"{metric.name}={metric.value}{metric.unit} ({','.join(f'{k}={v}' for k, v in metric.labels.items())})"
        for metric in state.metrics
    ])

    context = f"""
Incident: {state.incident_id}
Severity: {state.severity}
Description: {state.incident_description}

Recent Logs:
{logs_text}

Current Metrics:
{metrics_text}

Please analyze this incident and provide:
1. Root cause hypothesis
2. Confidence level (0.0-1.0)
3. List of affected services
4. List of contributing factors

Return as JSON only, no additional text.
"""

    # ==================== CALL LLM ====================
    llm_service = LLMService()

    llm_request = GenerateRequest(
        messages=[
            ChatMessage(
                role="system",
                content=(
                    "You are an expert incident response engineer. "
                    "Analyze the provided logs and metrics to determine root cause. "
                    "Be concise and precise. Return JSON."
                ),
            ),
            ChatMessage(role="user", content=context),
        ],
        model="qwen2.5-coder:7b",
        stream=False,
    )

    try:
        llm_response = await llm_service.generate_response(llm_request)
        analysis_text = llm_response.content

        # Parse JSON from response
        analysis_json = json.loads(analysis_text)

        state.root_cause = RootCauseAnalysis(
            hypothesis=analysis_json.get("hypothesis", "Unknown"),
            confidence=float(analysis_json.get("confidence", 0.5)),
            affected_services=analysis_json.get("affected_services", []),
            contributing_factors=analysis_json.get("contributing_factors", []),
        )
    except Exception as e:
        # If LLM call fails, populate with low-confidence analysis
        state.root_cause = RootCauseAnalysis(
            hypothesis=f"Analysis failed: {str(e)}",
            confidence=0.0,
            affected_services=[],
            contributing_factors=[],
        )

    return state

