"""
Test suite for main application functionality.

Tests basic API health checks and application startup.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

# Create test client with proper headers
client = TestClient(app, headers={"host": "localhost"})


def test_root_endpoint():
    """Test root endpoint returns expected response."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "DayPilot AI Scheduling API"
    assert data["version"] == "1.0.0"
    assert data["status"] == "operational"
    assert data["docs"] == "/api/docs"


def test_health_endpoint():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["version"] == "1.0.0"


def test_api_health_endpoint():
    """Test API v1 health endpoint."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["api_version"] == "v1"


def test_api_status_endpoint():
    """Test API v1 status endpoint."""
    response = client.get("/api/v1/status")
    assert response.status_code == 200
    data = response.json()
    assert data["api"] == "operational"
    assert data["version"] == "1.0.0"