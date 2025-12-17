"""
Task service for business logic operations with user isolation
"""
from typing import List, Optional, Dict, Any
from datetime import date, datetime
from sqlmodel import Session, select
from src.models.task import Task, TaskCreate, TaskUpdate, TaskCompletionUpdate


class TaskService:
    """
    Service class for task-related business logic with user isolation
    """

    @staticmethod
    def get_tasks_by_user_id(session: Session, user_id: int) -> List[Task]:
        """
        Get all tasks for a specific user
        """
        tasks = session.exec(
            select(Task).where(Task.user_id == user_id)
        ).all()
        return tasks

    @staticmethod
    def get_task_by_id_and_user_id(session: Session, task_id: int, user_id: int) -> Optional[Task]:
        """
        Get a specific task for a specific user
        """
        task = session.exec(
            select(Task).where(Task.id == task_id).where(Task.user_id == user_id)
        ).first()
        return task

    @staticmethod
    def create_task(session: Session, task_create: TaskCreate, user_id: int) -> Task:
        """
        Create a new task for a specific user
        """
        db_task = Task(
            **task_create.dict(),
            user_id=user_id
        )
        session.add(db_task)
        session.commit()
        session.refresh(db_task)
        return db_task

    @staticmethod
    def update_task(session: Session, task_id: int, task_update: TaskUpdate, user_id: int) -> Optional[Task]:
        """
        Update a specific task for a specific user
        """
        task = session.exec(
            select(Task).where(Task.id == task_id).where(Task.user_id == user_id)
        ).first()

        if not task:
            return None

        # Update task fields if they are provided
        update_data = task_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(task, field, value)

        # Update the timestamp
        from datetime import datetime
        task.updated_at = datetime.utcnow()

        session.add(task)
        session.commit()
        session.refresh(task)
        return task

    @staticmethod
    def update_task_completion(session: Session, task_id: int, completion_update: TaskCompletionUpdate, user_id: int) -> Optional[Task]:
        """
        Update the completion status of a specific task for a specific user
        """
        task = session.exec(
            select(Task).where(Task.id == task_id).where(Task.user_id == user_id)
        ).first()

        if not task:
            return None

        task.completed = completion_update.completed

        # Update the timestamp
        from datetime import datetime
        task.updated_at = datetime.utcnow()

        session.add(task)
        session.commit()
        session.refresh(task)
        return task

    @staticmethod
    def delete_task(session: Session, task_id: int, user_id: int) -> bool:
        """
        Delete a specific task for a specific user
        """
        task = session.exec(
            select(Task).where(Task.id == task_id).where(Task.user_id == user_id)
        ).first()

        if not task:
            return False

        session.delete(task)
        session.commit()
        return True

    @staticmethod
    def get_tasks_with_filters(
        session: Session,
        user_id: int,
        completed: Optional[bool] = None,
        priority: Optional[str] = None,
        overdue_only: bool = False
    ) -> List[Task]:
        """
        Get tasks for a user with optional filters (Phase 2).

        Args:
            session: Database session
            user_id: User ID for isolation
            completed: Filter by completion status (None = all)
            priority: Filter by priority level (High, Medium, Low)
            overdue_only: If True, return only overdue tasks

        Returns:
            List of filtered tasks
        """
        query = select(Task).where(Task.user_id == user_id)

        # Apply completion filter
        if completed is not None:
            query = query.where(Task.completed == completed)

        # Apply priority filter
        if priority:
            query = query.where(Task.priority == priority)

        # Apply overdue filter
        if overdue_only:
            today = date.today()
            query = query.where(Task.due_date < today).where(Task.completed == False)

        # Order by due date (nulls last), then created_at
        query = query.order_by(Task.due_date.asc(), Task.created_at.desc())

        tasks = session.exec(query).all()
        return tasks

    @staticmethod
    def get_task_statistics(session: Session, user_id: int) -> Dict[str, Any]:
        """
        Get task statistics for dashboard display (Phase 2).

        Args:
            session: Database session
            user_id: User ID for isolation

        Returns:
            Dictionary with task counts and statistics
        """
        all_tasks = session.exec(
            select(Task).where(Task.user_id == user_id)
        ).all()

        total = len(all_tasks)
        completed = sum(1 for task in all_tasks if task.completed)
        pending = total - completed

        # Count overdue tasks
        today = date.today()
        overdue = sum(
            1 for task in all_tasks
            if task.due_date and task.due_date < today and not task.completed
        )

        # Count by priority
        high_priority = sum(1 for task in all_tasks if task.priority == "High")
        medium_priority = sum(1 for task in all_tasks if task.priority == "Medium")
        low_priority = sum(1 for task in all_tasks if task.priority == "Low")

        return {
            "total": total,
            "completed": completed,
            "pending": pending,
            "overdue": overdue,
            "high_priority": high_priority,
            "medium_priority": medium_priority,
            "low_priority": low_priority
        }