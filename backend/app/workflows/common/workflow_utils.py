"""
Workflow Utilities

Helper functions for workflow management:
- State serialization/deserialization
- Logging node transitions
- Error handling
- State validation
"""

from typing import Any, Dict, Type, TypeVar
from app.workflows.common.base_state import BaseWorkflowState
from app.observability.logger import log_event
import logging

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseWorkflowState)


def state_to_dict(state: BaseWorkflowState) -> Dict[str, Any]:
    """
    Convert workflow state to dictionary for serialization.

    Args:
        state: Workflow state instance

    Returns:
        dict: Serializable state dictionary
    """
    return state.to_dict()


def dict_to_state(data: Dict[str, Any], state_class: Type[T]) -> T:
    """
    Deserialize dictionary to workflow state.

    Args:
        data: Serialized state dictionary
        state_class: State class to instantiate

    Returns:
        state_class: Deserialized state instance
    """
    return state_class.from_dict(data)


def log_node_transition(
    workflow_id: str,
    from_node: str,
    to_node: str,
    state: BaseWorkflowState,
    metadata: Dict[str, Any] = None,
):
    """
    Log a workflow node transition for observability.

    Args:
        workflow_id: Unique workflow run ID
        from_node: Previous node name
        to_node: Next node name
        state: Current workflow state
        metadata: Additional context to log
    """

    log_data = {
        "workflow_id": workflow_id,
        "workflow_type": state.workflow_type,
        "from_node": from_node,
        "to_node": to_node,
        "checkpoint": to_node,
        "status": state.status,
    }

    if metadata:
        log_data["metadata"] = metadata

    log_event("workflow_transition", log_data)
    logger.info(
        f"Workflow {workflow_id}: {from_node} → {to_node}",
        extra=log_data,
    )


def validate_state_transition(
    current_state: BaseWorkflowState,
    valid_next_statuses: list[str],
) -> bool:
    """
    Validate that a state can transition to next status.

    Args:
        current_state: Current workflow state
        valid_next_statuses: List of allowed next statuses

    Returns:
        bool: True if transition is valid
    """

    # Can only transition from "running" or "paused"
    if current_state.status not in ("running", "paused"):
        return False

    # Must transition to valid next status
    if any(next_status not in valid_next_statuses for next_status in valid_next_statuses):
        return False

    return True


def merge_state_updates(
    current_state: BaseWorkflowState,
    updates: Dict[str, Any],
) -> BaseWorkflowState:
    """
    Safely merge state updates.

    Only updates allowed fields, preserves immutable fields.

    Args:
        current_state: Current workflow state
        updates: Dictionary of field updates

    Returns:
        BaseWorkflowState: Updated state
    """

    # Immutable fields that cannot be updated
    immutable = {"workflow_type", "workflow_run_id", "created_at"}

    safe_updates = {
        k: v for k, v in updates.items()
        if k not in immutable
    }

    return current_state.copy(update=safe_updates)

