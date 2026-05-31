"""Task dispatcher.

Routes tasks to appropriate handlers.
Manages task execution, retries, and error handling.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Any, Optional
import asyncio

from app.queues.redis_queue import QueueJob, RedisQueue


@dataclass
class TaskHandler:
    """Handler for a specific task type."""

    task_name: str
    handler: Callable
    max_retries: int = 3
    timeout_seconds: int = 300


@dataclass
class TaskDispatcher:
    """Dispatches tasks to handlers."""

    queue: RedisQueue
    _handlers: dict[str, TaskHandler] = field(default_factory=dict)

    def register_handler(
        self,
        task_name: str,
        handler: Callable,
        max_retries: int = 3,
        timeout_seconds: int = 300,
    ):
        """Register a handler for a task type."""
        self._handlers[task_name] = TaskHandler(
            task_name=task_name,
            handler=handler,
            max_retries=max_retries,
            timeout_seconds=timeout_seconds,
        )

    async def process_tasks(self):
        """Process tasks from the queue."""
        while True:
            try:
                job = await self.queue.dequeue()
                if not job:
                    await asyncio.sleep(1)
                    continue

                await self._execute_job(job)
            except Exception as e:
                print(f"Error processing task: {e}")
                await asyncio.sleep(1)

    async def _execute_job(self, job: QueueJob):
        """Execute a single job."""
        handler = self._handlers.get(job.task_name)
        if not handler:
            print(f"No handler for task: {job.task_name}")
            await self.queue.mark_failed(job.job_id, f"No handler for {job.task_name}")
            return

        try:
            # Execute with timeout
            result = await asyncio.wait_for(
                handler.handler(**job.task_args),
                timeout=handler.timeout_seconds,
            )
            await self.queue.mark_complete(job.job_id, result)
        except asyncio.TimeoutError:
            await self.queue.mark_failed(job.job_id, "Task timeout")
        except Exception as e:
            await self.queue.mark_failed(job.job_id, str(e))

    async def dispatch(self, task_name: str, **kwargs) -> str:
        """Dispatch a task to the queue."""
        return await self.queue.enqueue(task_name, **kwargs)

