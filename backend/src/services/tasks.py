from sqlmodel import Session, select
from typing import List, Optional
from uuid import UUID
from datetime import datetime

from ..models.task import Task, TaskCreate
from ..models.user import User


def list_user_tasks(db: Session, user_id: UUID, skip: int = 0, limit: int = 50) -> List[Task]:
    """
    List all tasks for a specific user with pagination.
    """
    statement = (
        select(Task)
        .where(Task.user_id == user_id)
        .order_by(Task.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    return db.exec(statement).all()


def get_user_task(db: Session, task_id: UUID, user_id: UUID) -> Optional[Task]:
    """
    Get a specific task for a user.
    Returns the task only if it belongs to the user, None otherwise.
    """
    statement = select(Task).where(Task.id == task_id).where(Task.user_id == user_id)
    return db.exec(statement).first()


def create_task(db: Session, task_create: TaskCreate, user_id: UUID) -> Task:
    """
    Create a new task for a user.
    """
    db_task = Task(
        title=task_create.title,
        description=task_create.description,
        user_id=user_id,
        is_completed=getattr(task_create, 'is_completed', False)
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def update_task(db: Session, task_id: UUID, user_id: UUID, title: str = None, description: str = None) -> Optional[Task]:
    """
    Update a task for a user.
    Returns the updated task if successful, None if task doesn't exist or doesn't belong to user.
    """
    db_task = get_user_task(db, task_id, user_id)
    if not db_task:
        return None

    if title is not None:
        db_task.title = title
    if description is not None:
        db_task.description = description

    db_task.updated_at = datetime.utcnow()
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def delete_task(db: Session, task_id: UUID, user_id: UUID) -> bool:
    """
    Delete a task for a user.
    Returns True if successful, False if task doesn't exist or doesn't belong to user.
    """
    db_task = get_user_task(db, task_id, user_id)
    if not db_task:
        return False

    db.delete(db_task)
    db.commit()
    return True


def toggle_task_completion(db: Session, task_id: UUID, user_id: UUID) -> Optional[Task]:
    """
    Toggle the completion status of a task for a user.
    Returns the updated task if successful, None if task doesn't exist or doesn't belong to user.
    """
    db_task = get_user_task(db, task_id, user_id)
    if not db_task:
        return None

    db_task.is_completed = not db_task.is_completed
    db_task.updated_at = datetime.utcnow()
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def get_user_task_count(db: Session, user_id: UUID) -> int:
    """
    Get the total count of tasks for a user.
    """
    statement = select(Task).where(Task.user_id == user_id)
    return len(db.exec(statement).all())