"""Task queue package.

Async task queue for background job processing.
Built on Redis for distributed execution.

Usage:

from app.queues.redis_queue import RedisQueue
from app.queues.task_dispatcher import TaskDispatcher

# Setup
queue = RedisQueue(redis_url="redis://localhost:6379")
dispatcher = TaskDispatcher(queue)

# Register handler
async def send_email(to: str, subject: str):
    print(f"Sending email to {to}: {subject}")
    return "sent"

dispatcher.register_handler("send_email", send_email, max_retries=3)

# Dispatch task
job_id = await dispatcher.dispatch("send_email", to="user@example.com", subject="Hello")

# Process tasks (usually in separate worker process)
await dispatcher.process_tasks()
"""

from app.queues.redis_queue import RedisQueue, QueueJob
from app.queues.task_dispatcher import TaskDispatcher, TaskHandler

__all__ = [
    "RedisQueue",
    "QueueJob",
    "TaskDispatcher",
    "TaskHandler",
]

