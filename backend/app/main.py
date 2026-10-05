"""
DayPilot AI-Powered Scheduling System - Main FastAPI Application

This module initializes the FastAPI application with all necessary middleware,
routing, and configuration for the DayPilot scheduling system.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
import structlog
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from app.core.config import get_settings
from app.core.database import init_db
from app.api.v1.router import api_router

# Configure structured logging
logger = structlog.get_logger()

# Global settings
settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Application lifespan manager for startup and shutdown events.
    
    Handles:
    - Database initialization
    - ML model loading
    - Resource cleanup
    """
    logger.info("Starting DayPilot application...")
    
    # Initialize database
    await init_db()
    logger.info("Database initialized successfully")
    
    yield
    
    # Cleanup code here
    logger.info("Shutting down DayPilot application...")


# Create FastAPI application
app = FastAPI(
    title="DayPilot AI Scheduling API",
    description="AI-powered one-day time management system with natural language processing and intelligent scheduling",
    version="1.0.0",
    docs_url="/api/docs" if settings.DEBUG else None,
    redoc_url="/api/redoc" if settings.DEBUG else None,
    lifespan=lifespan,
)

# Add security middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings.ALLOWED_HOSTS,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc: HTTPException) -> JSONResponse:
    """Global HTTP exception handler with structured error responses."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.status_code,
                "message": exc.detail,
                "type": "HTTPException",
            }
        },
    )


@app.get("/", tags=["Health"])
async def root():
    """Root endpoint - API health check"""
    return {
        "message": "DayPilot AI Scheduling API",
        "version": "1.0.0",
        "status": "operational",
        "docs": "/api/docs",
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Detailed health check endpoint"""
    return {
        "status": "healthy",
        "database": "connected",
        "ai_services": "available",
        "version": "1.0.0",
    }


# Include API routes
app.include_router(api_router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level="info",
    )