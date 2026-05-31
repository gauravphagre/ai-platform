"""Evaluation frameworks.

This package contains evaluation harnesses for:
- Retrieval: RAG retrieval quality metrics
- Workflows: Workflow correctness and performance
- Hallucination: LLM hallucination detection
- Tool Accuracy: Tool call accuracy and safety
"""

from app.evals.retrieval.retrieval_eval import RetrievalEvaluator
from app.evals.workflows.workflow_eval import WorkflowEvaluator
from app.evals.hallucination.hallucination_eval import HallucinationDetector
from app.evals.tool_accuracy.tool_eval import ToolAccuracyEvaluator

__all__ = [
    "RetrievalEvaluator",
    "WorkflowEvaluator",
    "HallucinationDetector",
    "ToolAccuracyEvaluator",
]

