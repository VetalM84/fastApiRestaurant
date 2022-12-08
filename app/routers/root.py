"""GET endpoints for root."""

from fastapi import APIRouter

router = APIRouter(prefix="", tags=["root"])


@router.get("/", description="Check health server status.", tags=["API status"])
async def root():
    return {"message": "Server is OK"}
