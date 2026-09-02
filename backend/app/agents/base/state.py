"""Shared agent/workflow state helpers.

Kept minimal; workflows already define their own state models.
"""

from __future__ import annotations

from typing import Any, Protocol


class SupportsDict(Protocol):
    def model_dump(self, *args: Any, **kwargs: Any) -> dict[str, Any]: ...

