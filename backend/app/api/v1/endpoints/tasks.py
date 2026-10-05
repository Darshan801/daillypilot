"""
Task management API endpoints.

Provides CRUD operations for tasks including creation, retrieval,
updating, completion, and deletion.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
import structlog

from app.core.database import get_db
from app.services.task_service import TaskService
from app.schemas.task_schemas import (
    TaskCreateRequest,
    TaskUpdateRequest, 
    TaskCompleteRequest,
    TaskResponse,
    TaskListResponse,
    TaskStatsResponse,
    ErrorResponse,
)
from app.models.task import TaskCategory, PriorityLevel

logger = structlog.get_logger()
router = APIRouter()

# TODO: Add proper authentication and get user_id from JWT token
# For now, using a default user ID for development
DEFAULT_USER_ID = "dev_user_123"


@router.post(
    "/",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task",
    description="Create a new task for the authenticated user",
)
async def create_task(
    task_data: TaskCreateRequest,
    db: AsyncSession = Depends(get_db)
) -> TaskResponse:
    """
    Create a new task.
    
    - **name**: Task name (required, 1-200 characters)
    - **description**: Optional task description (max 1000 characters)
    - **estimated_duration_minutes**: Estimated completion time (1-480 minutes)
    - **priority**: Task priority level (low, medium, high, urgent)
    - **category**: Task category for ML features
    - **flexibility**: How flexible the task timing is
    - **energy_requirement**: Energy level required for the task
    - **constraints**: Optional scheduling constraints as JSON
    """
    try:
        task = await TaskService.create_task(
            db=db,
            user_id=DEFAULT_USER_ID,
            name=task_data.name,
            description=task_data.description,
            estimated_duration_minutes=task_data.estimated_duration_minutes,
            priority=task_data.priority,
            category=task_data.category,
            flexibility=task_data.flexibility,
            energy_requirement=task_data.energy_requirement,
            constraints=task_data.constraints,
        )
        
        await db.commit()
        logger.info(f"Created task {task.id}: {task.name}")
        return TaskResponse.model_validate(task)
        
    except Exception as e:
        await db.rollback()
        logger.error(f"Error creating task: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create task: {str(e)}"
        )


@router.get(
    "/",
    response_model=TaskListResponse,
    summary="Get user tasks",
    description="Retrieve tasks for the authenticated user with optional filtering",
)
async def get_tasks(
    include_completed: bool = Query(False, description="Include completed tasks"),
    category: Optional[TaskCategory] = Query(None, description="Filter by task category"),
    priority: Optional[PriorityLevel] = Query(None, description="Filter by priority level"),
    limit: int = Query(50, ge=1, le=100, description="Maximum number of tasks to return"),
    offset: int = Query(0, ge=0, description="Number of tasks to skip"),
    db: AsyncSession = Depends(get_db)
) -> TaskListResponse:
    """
    Get tasks for the authenticated user.
    
    Query parameters:
    - **include_completed**: Whether to include completed tasks (default: false)
    - **category**: Filter by task category (optional)
    - **priority**: Filter by priority level (optional)
    - **limit**: Maximum number of tasks (1-100, default: 50)
    - **offset**: Number of tasks to skip (default: 0)
    """
    try:
        tasks = await TaskService.get_user_tasks(
            db=db,
            user_id=DEFAULT_USER_ID,
            include_completed=include_completed,
            category=category,
            priority=priority,
            limit=limit,
            offset=offset,
        )
        
        # For simplicity, returning len(tasks) as total_count
        # In production, you'd want a separate count query
        return TaskListResponse(
            tasks=[TaskResponse.model_validate(task) for task in tasks],
            total_count=len(tasks),
            offset=offset,
            limit=limit,
        )
        
    except Exception as e:
        logger.error(f"Error retrieving tasks: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve tasks: {str(e)}"
        )


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Get a specific task",
    description="Retrieve a specific task by its ID",
)
async def get_task(
    task_id: str,
    db: AsyncSession = Depends(get_db)
) -> TaskResponse:
    """
    Get a specific task by ID.
    
    - **task_id**: The unique identifier of the task
    """
    task = await TaskService.get_task(
        db=db,
        task_id=task_id,
        user_id=DEFAULT_USER_ID,
    )
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    return TaskResponse.model_validate(task)


@router.put(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Update a task",
    description="Update an existing task with new values",
)
async def update_task(
    task_id: str,
    task_updates: TaskUpdateRequest,
    db: AsyncSession = Depends(get_db)
) -> TaskResponse:
    """
    Update an existing task.
    
    - **task_id**: The unique identifier of the task
    - Only provided fields will be updated
    """
    try:
        # Convert Pydantic model to dict, excluding None values
        updates = task_updates.model_dump(exclude_none=True)
        
        if not updates:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No valid fields provided for update"
            )
        
        task = await TaskService.update_task(
            db=db,
            task_id=task_id,
            user_id=DEFAULT_USER_ID,
            updates=updates,
        )
        
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        
        await db.commit()
        logger.info(f"Updated task {task_id}")
        return TaskResponse.model_validate(task)
        
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        logger.error(f"Error updating task {task_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update task: {str(e)}"
        )


@router.post(
    "/{task_id}/complete",
    response_model=TaskResponse,
    summary="Complete a task",
    description="Mark a task as completed with optional actual duration",
)
async def complete_task(
    task_id: str,
    completion_data: TaskCompleteRequest,
    db: AsyncSession = Depends(get_db)
) -> TaskResponse:
    """
    Mark a task as completed.
    
    - **task_id**: The unique identifier of the task
    - **actual_duration_minutes**: Optional actual time taken to complete
    """
    try:
        task = await TaskService.complete_task(
            db=db,
            task_id=task_id,
            user_id=DEFAULT_USER_ID,
            actual_duration_minutes=completion_data.actual_duration_minutes,
        )
        
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        
        await db.commit()
        logger.info(f"Completed task {task_id}")
        return TaskResponse.model_validate(task)
        
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        logger.error(f"Error completing task {task_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to complete task: {str(e)}"
        )


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a task",
    description="Delete a specific task by its ID",
)
async def delete_task(
    task_id: str,
    db: AsyncSession = Depends(get_db)
) -> None:
    """
    Delete a task.
    
    - **task_id**: The unique identifier of the task to delete
    """
    try:
        success = await TaskService.delete_task(
            db=db,
            task_id=task_id,
            user_id=DEFAULT_USER_ID,
        )
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        
        await db.commit()
        logger.info(f"Deleted task {task_id}")
        
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        logger.error(f"Error deleting task {task_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete task: {str(e)}"
        )