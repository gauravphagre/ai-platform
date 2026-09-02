"""Workflow run repository.

Persists workflow runs (including incident workflows) to the database.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.models.workflow_run import WorkflowRun


@dataclass
class WorkflowRunRepository:
    db: AsyncSession

    async def create_run(
        self,
        workflow_id: str,
        workflow_type: str,
        status: str,
        state: dict[str, Any],
    ) -> WorkflowRun:
        run = WorkflowRun(
            workflow_id=workflow_id,
            workflow_type=workflow_type,
            status=status,
            state=state,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        self.db.add(run)
        await self.db.commit()
        await self.db.refresh(run)
        return run

    async def get_run(self, workflow_id: str) -> Optional[WorkflowRun]:
        result = await self.db.execute(
            select(WorkflowRun).where(WorkflowRun.workflow_id == workflow_id)
        )
        return result.scalar_one_or_none()

    async def update_run(
        self,
        workflow_id: str,
        *,
        status: Optional[str] = None,
        state: Optional[dict[str, Any]] = None,
    ) -> Optional[WorkflowRun]:
        run = await self.get_run(workflow_id)
        if not run:
            return None

        if status is not None:
            run.status = status
        if state is not None:
            run.state = state

        run.updated_at = datetime.utcnow()
        self.db.add(run)
        await self.db.commit()
        await self.db.refresh(run)
        return run

