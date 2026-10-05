"""
Main API router for DayPilot v1 endpoints.

Aggregates all API route modules and provides a single router for the main application.
"""

from fastapi import APIRouter

# Create main API router
api_router = APIRouter()

# Health check endpoints (temporary until full implementation)
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

# TODO: Add task parsing endpoints
# TODO: Add scheduling endpoints  
# TODO: Add ML endpoints
# TODO: Add explanation endpoints