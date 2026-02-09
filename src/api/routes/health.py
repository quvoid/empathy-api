from fastapi import APIRouter
from src.core.config import get_config

router = APIRouter()


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    config = get_config()
    return {"status": "healthy", "service": config.APP_NAME, "version": "1.0.0"}
