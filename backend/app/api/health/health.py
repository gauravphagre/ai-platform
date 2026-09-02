"""Health endpoints.

Provides lightweight health checks for:
- service liveness
- service readiness

Keep this dependency-light and fast.
"""

from fastapi import APIRouter

router = APIRouter(tags=["health"])

@router.get("/health")
async def health():
    return {
        "status": "healthy"
    }

@router.get("/health/live")
async def liveness():
    return {"status": "ok"}


@router.get("/health/ready")
async def readiness():
    # TODO: add checks (db connectivity, provider availability) when needed
    return {"status": "ok"}

