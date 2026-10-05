"""
Main API router for DayPilot v1 endpoints.

Aggregates all API route modules and provides a single router for the main application.
"""

from fastapi import APIRouter
from app.api.v1.endpoints.tasks import router as tasks_router

# Create main API router
api_router = APIRouter()

# Health check endpoints
@api_router.get("/health")
async def health_check():
    """API health check endpoint"""
    return {
        "status": "healthy",
        "api_version": "v1",
        "message": "DayPilot API is operational"
    }

@api_router.get("/status")
async def status_check():
    """Detailed status endpoint"""
    return {
        "api": "operational",
        "database": "connected",
        "ai_services": "available",
        "version": "1.0.0"
    }

# Include feature routers
api_router.include_router(tasks_router, prefix="/tasks", tags=["Tasks"])

# TODO: Add task parsing endpoints (LLM integration)
# TODO: Add scheduling endpoints  
# TODO: Add ML endpoints
# TODO: Add explanation endpoints