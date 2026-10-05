"""
Pydantic schemas for task-related API operations.

Defines request and response models for task management endpoints.
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
from enum import Enum

from app.models.task import PriorityLevel, TaskCategory, FlexibilityLevel, EnergyLevel


class TaskCreateRequest(BaseModel):
    """Request schema for creating a new task."""
    
    name: str = Field(..., min_length=1, max_length=200, description="Task name or title")
    description: Optional[str] = Field(None, max_length=1000, description="Optional task description")
    estimated_duration_minutes: int = Field(30, ge=1, le=480, description="Estimated duration in minutes (1-480)")
    priority: PriorityLevel = Field(PriorityLevel.MEDIUM, description="Task priority level")
    category: TaskCategory = Field(TaskCategory.OTHER, description="Task category for ML features")
    flexibility: FlexibilityLevel = Field(FlexibilityLevel.FLEXIBLE, description="Task timing flexibility")
    energy_requirement: EnergyLevel = Field(EnergyLevel.MEDIUM, description="Energy level required")
    constraints: Optional[Dict[str, Any]] = Field(None, description="Optional scheduling constraints")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Review quarterly reports",
                "description": "Go through Q3 financial reports and prepare summary",
                "estimated_duration_minutes": 60,
                "priority": "high",
                "category": "work",
                "flexibility": "flexible",
                "energy_requirement": "medium",
                "constraints": {
                    "deadline": "2024-01-15T17:00:00Z",
                    "preferred_time": "morning"
                }
            }
        }
    )


class TaskUpdateRequest(BaseModel):
    """Request schema for updating an existing task."""
    
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    estimated_duration_minutes: Optional[int] = Field(None, ge=1, le=480)
    priority: Optional[PriorityLevel] = None
    category: Optional[TaskCategory] = None
    flexibility: Optional[FlexibilityLevel] = None
    energy_requirement: Optional[EnergyLevel] = None
    constraints: Optional[Dict[str, Any]] = None
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Review quarterly reports (updated)",
                "priority": "urgent",
                "estimated_duration_minutes": 90
            }
        }
    )


class TaskCompleteRequest(BaseModel):
    """Request schema for completing a task."""
    
    actual_duration_minutes: Optional[int] = Field(
        None, 
        ge=1, 
        le=480, 
        description="Actual time taken to complete the task"
    )
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "actual_duration_minutes": 75
            }
        }
    )


class TaskResponse(BaseModel):
    """Response schema for task data."""
    
    id: str
    user_id: str
    name: str
    description: Optional[str] = None
    estimated_duration_minutes: int
    priority: PriorityLevel
    category: TaskCategory
    flexibility: FlexibilityLevel
    energy_requirement: EnergyLevel
    constraints: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime
    is_completed: bool
    completed_at: Optional[datetime] = None
    actual_duration_minutes: Optional[int] = None
    parsing_confidence: Optional[float] = None
    original_text: Optional[str] = None
    
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "user_id": "user123",
                "name": "Review quarterly reports",
                "description": "Go through Q3 financial reports and prepare summary",
                "estimated_duration_minutes": 60,
                "priority": "high",
                "category": "work",
                "flexibility": "flexible",
                "energy_requirement": "medium",
                "constraints": {
                    "deadline": "2024-01-15T17:00:00Z",
                    "preferred_time": "morning"
                },
                "created_at": "2024-01-10T09:00:00Z",
                "updated_at": "2024-01-10T09:00:00Z",
                "is_completed": False,
                "completed_at": None,
                "actual_duration_minutes": None,
                "parsing_confidence": None,
                "original_text": None
            }
        }
    )


class TaskListResponse(BaseModel):
    """Response schema for list of tasks."""
    
    tasks: List[TaskResponse]
    total_count: int
    offset: int
    limit: int
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "tasks": [
                    # Task objects here
                ],
                "total_count": 25,
                "offset": 0,
                "limit": 10
            }
        }
    )


class TaskStatsResponse(BaseModel):
    """Response schema for task statistics."""
    
    total_tasks: int
    completed_tasks: int
    pending_tasks: int
    overdue_tasks: int
    average_completion_time_minutes: Optional[float] = None
    completion_rate: float
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "total_tasks": 50,
                "completed_tasks": 35,
                "pending_tasks": 15,
                "overdue_tasks": 2,
                "average_completion_time_minutes": 45.5,
                "completion_rate": 0.7
            }
        }
    )


class ErrorResponse(BaseModel):
    """Standard error response schema."""
    
    error: str
    message: str
    details: Optional[Dict[str, Any]] = None
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "error": "ValidationError",
                "message": "Task name is required",
                "details": {
                    "field": "name",
                    "code": "missing"
                }
            }
        }
    )