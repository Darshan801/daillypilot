"""
Task service for managing task operations.

Handles CRUD operations, validation, and business logic for tasks.
"""

from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload
import uuid
import structlog

from app.models.task import Task, PriorityLevel, TaskCategory, FlexibilityLevel, EnergyLevel
from app.models.user_context import UserContext

logger = structlog.get_logger()


class TaskService:
    """Service for managing tasks and task-related operations."""
    
    @staticmethod
    async def create_task(
        db: AsyncSession,
        user_id: str,
        name: str,
        description: Optional[str] = None,
        estimated_duration_minutes: int = 30,
        priority: PriorityLevel = PriorityLevel.MEDIUM,
        category: TaskCategory = TaskCategory.OTHER,
        flexibility: FlexibilityLevel = FlexibilityLevel.FLEXIBLE,
        energy_requirement: EnergyLevel = EnergyLevel.MEDIUM,
        constraints: Optional[Dict[str, Any]] = None,
        original_text: Optional[str] = None,
        parsing_confidence: Optional[float] = None,
    ) -> Task:
        """
        Create a new task in the database.
        
        Args:
            db: Database session
            user_id: ID of the user creating the task
            name: Task name/title
            description: Optional task description
            estimated_duration_minutes: Estimated completion time in minutes
            priority: Task priority level
            category: Task category for ML features
            flexibility: How flexible the task timing is
            energy_requirement: Energy level required for task
            constraints: Optional constraints (JSON)
            original_text: Original natural language input
            parsing_confidence: AI parsing confidence score
        
        Returns:
            Created Task object
        """
        task = Task(
            id=str(uuid.uuid4()),
            user_id=user_id,
            name=name,
            description=description,
            estimated_duration_minutes=estimated_duration_minutes,
            priority=priority,
            category=category,
            flexibility=flexibility,
            energy_requirement=energy_requirement,
            constraints=constraints or {},
            original_text=original_text,
            parsing_confidence=parsing_confidence,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        
        db.add(task)
        await db.flush()  # Get the ID without committing
        await db.refresh(task)
        
        logger.info(f"Created task {task.id} for user {user_id}: {name}")
        return task
    
    @staticmethod
    async def get_task(
        db: AsyncSession,
        task_id: str,
        user_id: str,
    ) -> Optional[Task]:
        """
        Get a task by ID, ensuring it belongs to the user.
        
        Args:
            db: Database session
            task_id: Task ID to retrieve
            user_id: User ID for authorization
        
        Returns:
            Task object if found and authorized, None otherwise
        """
        result = await db.execute(
            select(Task).where(
                Task.id == task_id,
                Task.user_id == user_id
            )
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_user_tasks(
        db: AsyncSession,
        user_id: str,
        include_completed: bool = False,
        category: Optional[TaskCategory] = None,
        priority: Optional[PriorityLevel] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[Task]:
        """
        Get tasks for a user with optional filtering.
        
        Args:
            db: Database session
            user_id: User ID to get tasks for
            include_completed: Whether to include completed tasks
            category: Optional category filter
            priority: Optional priority filter
            limit: Maximum number of tasks to return
            offset: Number of tasks to skip
        
        Returns:
            List of Task objects
        """
        query = select(Task).where(Task.user_id == user_id)
        
        if not include_completed:
            query = query.where(Task.is_completed == False)
        
        if category:
            query = query.where(Task.category == category)
        
        if priority:
            query = query.where(Task.priority == priority)
        
        query = query.order_by(Task.created_at.desc()).limit(limit).offset(offset)
        
        result = await db.execute(query)
        return list(result.scalars().all())
    
    @staticmethod
    async def update_task(
        db: AsyncSession,
        task_id: str,
        user_id: str,
        updates: Dict[str, Any],
    ) -> Optional[Task]:
        """
        Update a task with new values.
        
        Args:
            db: Database session
            task_id: Task ID to update
            user_id: User ID for authorization
            updates: Dictionary of fields to update
        
        Returns:
            Updated Task object if successful, None if not found/authorized
        """
        # First check if task exists and belongs to user
        task = await TaskService.get_task(db, task_id, user_id)
        if not task:
            return None
        
        # Update the task
        updates["updated_at"] = datetime.utcnow()
        
        await db.execute(
            update(Task).where(
                Task.id == task_id,
                Task.user_id == user_id
            ).values(**updates)
        )
        
        # Fetch updated task
        await db.refresh(task)
        logger.info(f"Updated task {task_id} for user {user_id}")
        return task
    
    @staticmethod
    async def complete_task(
        db: AsyncSession,
        task_id: str,
        user_id: str,
        actual_duration_minutes: Optional[int] = None,
    ) -> Optional[Task]:
        """
        Mark a task as completed.
        
        Args:
            db: Database session
            task_id: Task ID to complete
            user_id: User ID for authorization
            actual_duration_minutes: Actual time taken to complete the task
        
        Returns:
            Updated Task object if successful, None if not found/authorized
        """
        updates = {
            "is_completed": True,
            "completed_at": datetime.utcnow(),
        }
        
        if actual_duration_minutes is not None:
            updates["actual_duration_minutes"] = actual_duration_minutes
        
        return await TaskService.update_task(db, task_id, user_id, updates)
    
    @staticmethod
    async def delete_task(
        db: AsyncSession,
        task_id: str,
        user_id: str,
    ) -> bool:
        """
        Delete a task.
        
        Args:
            db: Database session
            task_id: Task ID to delete
            user_id: User ID for authorization
        
        Returns:
            True if deleted successfully, False if not found/authorized
        """
        # Check if task exists and belongs to user
        task = await TaskService.get_task(db, task_id, user_id)
        if not task:
            return False
        
        await db.execute(
            delete(Task).where(
                Task.id == task_id,
                Task.user_id == user_id
            )
        )
        
        logger.info(f"Deleted task {task_id} for user {user_id}")
        return True