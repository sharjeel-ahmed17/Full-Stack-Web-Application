from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from uuid import UUID
from typing import List

from ...models.task import Task, TaskCreate
from ...models.user import User
from ...schemas.task import TaskCreateRequest, TaskUpdateRequest, TaskResponse, TaskListResponse, TaskToggleResponse
from ...api.deps import get_db, get_current_user
from datetime import datetime

tasks_router = APIRouter()


@tasks_router.get("/", response_model=TaskListResponse)
def list_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 50
):
    """
    List all tasks for the current user.
    """
    # Get tasks for the current user only
    statement = (
        select(Task)
        .where(Task.user_id == current_user.id)
        .order_by(Task.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    tasks = db.exec(statement).all()

    # Count total tasks for the user
    count_statement = select(Task).where(Task.user_id == current_user.id)
    total = len(db.exec(count_statement).all())

    task_responses = [
        TaskResponse(
            id=task.id,
            title=task.title,
            description=task.description,
            user_id=task.user_id,
            is_completed=task.is_completed,
            created_at=task.created_at,
            updated_at=task.updated_at
        )
        for task in tasks
    ]

    return TaskListResponse(tasks=task_responses, total=total)


@tasks_router.post("/", response_model=TaskResponse)
def create_task(
    task_data: TaskCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new task for the current user.
    """
    # Create task with current user's ID
    db_task = Task(
        title=task_data.title,
        description=task_data.description,
        user_id=current_user.id,
        is_completed=False
    )

    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    return TaskResponse(
        id=db_task.id,
        title=db_task.title,
        description=db_task.description,
        user_id=db_task.user_id,
        is_completed=db_task.is_completed,
        created_at=db_task.created_at,
        updated_at=db_task.updated_at
    )


@tasks_router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get a specific task by ID.
    Returns 404 if the task doesn't exist or doesn't belong to the current user.
    """
    # Find task that belongs to the current user
    statement = select(Task).where(Task.id == task_id).where(Task.user_id == current_user.id)
    task = db.exec(statement).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return TaskResponse(
        id=task.id,
        title=task.title,
        description=task.description,
        user_id=task.user_id,
        is_completed=task.is_completed,
        created_at=task.created_at,
        updated_at=task.updated_at
    )


@tasks_router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: UUID,
    task_data: TaskUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update a specific task by ID.
    Returns 404 if the task doesn't exist or doesn't belong to the current user.
    """
    # Find task that belongs to the current user
    statement = select(Task).where(Task.id == task_id).where(Task.user_id == current_user.id)
    task = db.exec(statement).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Update task fields if provided
    if task_data.title is not None:
        task.title = task_data.title
    if task_data.description is not None:
        task.description = task_data.description

    # Update the timestamp
    task.updated_at = datetime.utcnow()

    db.add(task)
    db.commit()
    db.refresh(task)

    return TaskResponse(
        id=task.id,
        title=task.title,
        description=task.description,
        user_id=task.user_id,
        is_completed=task.is_completed,
        created_at=task.created_at,
        updated_at=task.updated_at
    )


@tasks_router.delete("/{task_id}")
def delete_task(
    task_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete a specific task by ID.
    Returns 404 if the task doesn't exist or doesn't belong to the current user.
    """
    # Find task that belongs to the current user
    statement = select(Task).where(Task.id == task_id).where(Task.user_id == current_user.id)
    task = db.exec(statement).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    db.delete(task)
    db.commit()

    return {"message": "Task deleted successfully"}


@tasks_router.patch("/{task_id}/complete", response_model=TaskToggleResponse)
def toggle_task_completion(
    task_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Toggle the completion status of a task.
    Returns 404 if the task doesn't exist or doesn't belong to the current user.
    """
    # Find task that belongs to the current user
    statement = select(Task).where(Task.id == task_id).where(Task.user_id == current_user.id)
    task = db.exec(statement).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Toggle completion status
    task.is_completed = not task.is_completed
    task.updated_at = datetime.utcnow()

    db.add(task)
    db.commit()
    db.refresh(task)

    return TaskToggleResponse(
        id=task.id,
        is_completed=task.is_completed,
        updated_at=task.updated_at
    )