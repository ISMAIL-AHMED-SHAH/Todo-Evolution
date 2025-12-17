"""
Task management API endpoints with Phase 2 enhancements
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session
from typing import Any, List, Optional

from src.database import get_session
from src.models.task import Task
from src.schemas.task import TaskCreate, TaskUpdate, TaskResponse, TaskCompletionUpdate
from src.schemas.errors import NotFoundError, ForbiddenError
from src.auth.jwt_handler import jwt_bearer, get_user_id_from_token
from src.services.task_service import TaskService


router = APIRouter(prefix="/api", tags=["Tasks"])


@router.get("/{user_id}/tasks", response_model=List[TaskResponse])
async def get_tasks(
    user_id: int,
    completed: Optional[bool] = Query(None, description="Filter by completion status"),
    priority: Optional[str] = Query(None, description="Filter by priority (High, Medium, Low)"),
    overdue_only: bool = Query(False, description="Return only overdue tasks"),
    payload: dict = Depends(jwt_bearer),
    session: Session = Depends(get_session)
) -> Any:
    """
    Get all tasks for a specific user with optional filters (Phase 2).

    Supports filtering by:
    - completion status
    - priority level
    - overdue status
    """
    # Extract user ID from JWT token
    token_user_id = payload.get('sub') or payload.get('userId') or payload.get('user_id')

    # Verify that the requested user ID matches the authenticated user ID
    if str(user_id) != str(token_user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only access your own tasks"
        )

    # Get tasks with filters
    tasks = TaskService.get_tasks_with_filters(
        session,
        user_id,
        completed=completed,
        priority=priority,
        overdue_only=overdue_only
    )

    # Add computed fields to each task
    response_tasks = []
    for task in tasks:
        task_dict = task.model_dump()
        task_dict['is_overdue'] = task.is_overdue()
        task_dict['days_until_due'] = task.days_until_due()
        response_tasks.append(TaskResponse(**task_dict))

    return response_tasks


@router.post("/{user_id}/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    user_id: int,
    task_create: TaskCreate,
    payload: dict = Depends(jwt_bearer),
    session: Session = Depends(get_session)
) -> Any:
    """
    Create a new task for a specific user with Phase 2 fields.

    Required fields:
    - title

    Optional fields:
    - description
    - priority (High, Medium, Low) - defaults to Medium
    - category (array of strings)
    - due_date (YYYY-MM-DD format)
    """
    # Extract user ID from JWT token
    token_user_id = payload.get('sub') or payload.get('userId') or payload.get('user_id')

    # Verify that the requested user ID matches the authenticated user ID
    if str(user_id) != str(token_user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only create tasks for yourself"
        )

    # Create task from Pydantic model
    from src.models.task import Task as TaskModel, TaskCreate as TaskCreateModel
    task_data = task_create.model_dump()
    task_model = TaskCreateModel(**task_data)

    # Create new task using the service
    db_task = TaskService.create_task(session, task_model, user_id)

    # Build response with computed fields
    task_dict = db_task.model_dump()
    task_dict['is_overdue'] = db_task.is_overdue()
    task_dict['days_until_due'] = db_task.days_until_due()

    return TaskResponse(**task_dict)


@router.get("/{user_id}/tasks/{id}", response_model=TaskResponse)
async def get_task(
    user_id: int,
    id: int,
    payload: dict = Depends(jwt_bearer),
    session: Session = Depends(get_session)
) -> Any:
    """
    Get a specific task by ID for a specific user.
    """
    # Extract user ID from JWT token
    token_user_id = payload.get('sub') or payload.get('userId') or payload.get('user_id')

    # Verify that the requested user ID matches the authenticated user ID
    if str(user_id) != str(token_user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only access your own tasks"
        )

    # Get the specific task using the service
    task = TaskService.get_task_by_id_and_user_id(session, id, user_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Build response with computed fields
    task_dict = task.model_dump()
    task_dict['is_overdue'] = task.is_overdue()
    task_dict['days_until_due'] = task.days_until_due()

    return TaskResponse(**task_dict)


@router.put("/{user_id}/tasks/{id}", response_model=TaskResponse)
async def update_task(
    user_id: int,
    id: int,
    task_update: TaskUpdate,
    payload: dict = Depends(jwt_bearer),
    session: Session = Depends(get_session)
) -> Any:
    """
    Update a specific task for a specific user.

    Can update any combination of:
    - title
    - description
    - priority (High, Medium, Low)
    - category (array of strings)
    - due_date (YYYY-MM-DD format)
    - completed (boolean)
    """
    # Extract user ID from JWT token
    token_user_id = payload.get('sub') or payload.get('userId') or payload.get('user_id')

    # Verify that the requested user ID matches the authenticated user ID
    if str(user_id) != str(token_user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own tasks"
        )

    # Convert Pydantic schema to SQLModel schema
    from src.models.task import TaskUpdate as TaskUpdateModel
    task_data = task_update.model_dump(exclude_unset=True)
    task_model = TaskUpdateModel(**task_data)

    # Update task using the service
    updated_task = TaskService.update_task(session, id, task_model, user_id)
    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Build response with computed fields
    task_dict = updated_task.model_dump()
    task_dict['is_overdue'] = updated_task.is_overdue()
    task_dict['days_until_due'] = updated_task.days_until_due()

    return TaskResponse(**task_dict)


@router.delete("/{user_id}/tasks/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    user_id: int,
    id: int,
    payload: dict = Depends(jwt_bearer),
    session: Session = Depends(get_session)
) -> None:
    """
    Delete a specific task for a specific user.
    Returns 204 No Content on success.
    """
    # Extract user ID from JWT token
    token_user_id = payload.get('sub') or payload.get('userId') or payload.get('user_id')

    # Verify that the requested user ID matches the authenticated user ID
    if str(user_id) != str(token_user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own tasks"
        )

    # Delete task using the service
    success = TaskService.delete_task(session, id, user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Return 204 No Content (no response body)
    return None


@router.patch("/{user_id}/tasks/{id}/complete", response_model=TaskResponse)
async def toggle_task_completion(
    user_id: int,
    id: int,
    payload: dict = Depends(jwt_bearer),
    session: Session = Depends(get_session)
) -> Any:
    """
    Toggle task completion status (Phase 2).

    Automatically toggles the completed field and updates the timestamp.
    """
    # Extract user ID from JWT token
    token_user_id = payload.get('sub') or payload.get('userId') or payload.get('user_id')

    # Verify that the requested user ID matches the authenticated user ID
    if str(user_id) != str(token_user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own tasks"
        )

    # Get the task first to toggle its completion status
    task = TaskService.get_task_by_id_and_user_id(session, id, user_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Toggle completion status
    from src.models.task import TaskCompletionUpdate
    completion_update = TaskCompletionUpdate(completed=not task.completed)

    # Update task completion using the service
    updated_task = TaskService.update_task_completion(session, id, completion_update, user_id)
    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Build response with computed fields
    task_dict = updated_task.model_dump()
    task_dict['is_overdue'] = updated_task.is_overdue()
    task_dict['days_until_due'] = updated_task.days_until_due()

    return TaskResponse(**task_dict)