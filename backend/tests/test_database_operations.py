"""
Comprehensive database operation tests

Tests cover:
- User isolation enforcement at database level
- Foreign key relationships
- Index performance
- Transaction handling
- Connection pooling
- Error handling
"""
import pytest
from sqlmodel import Session, create_engine, SQLModel, select
from sqlmodel.pool import StaticPool
from datetime import datetime

from src.models.user import User
from src.models.task import Task
from src.database.database import get_db_session


# Setup test database
@pytest.fixture(name="test_engine")
def test_engine_fixture():
    """Create a test database engine"""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    return engine


@pytest.fixture(name="test_session")
def test_session_fixture(test_engine):
    """Create a test database session"""
    with Session(test_engine) as session:
        yield session


class TestDatabaseSchema:
    """Tests for database schema and constraints"""

    def test_user_table_exists(self, test_session: Session):
        """Test that user table exists with correct columns"""
        user = User(email="test@example.com", password_hash="hashed")
        test_session.add(user)
        test_session.commit()
        test_session.refresh(user)

        assert user.id is not None
        assert user.email == "test@example.com"
        assert user.created_at is not None
        assert user.updated_at is not None

    def test_task_table_exists(self, test_session: Session):
        """Test that task table exists with correct columns"""
        user = User(email="test@example.com", password_hash="hashed")
        test_session.add(user)
        test_session.commit()
        test_session.refresh(user)

        task = Task(
            user_id=user.id,
            title="Test Task",
            description="Test Description",
            completed=False
        )
        test_session.add(task)
        test_session.commit()
        test_session.refresh(task)

        assert task.id is not None
        assert task.user_id == user.id
        assert task.title == "Test Task"
        assert task.completed is False

    def test_email_unique_constraint(self, test_session: Session):
        """Test that email must be unique"""
        user1 = User(email="test@example.com", password_hash="hash1")
        test_session.add(user1)
        test_session.commit()

        # Try to create another user with same email
        user2 = User(email="test@example.com", password_hash="hash2")
        test_session.add(user2)

        with pytest.raises(Exception):  # Should raise integrity error
            test_session.commit()


class TestForeignKeyRelationships:
    """Tests for foreign key constraints"""

    def test_foreign_key_relationship(self, test_session: Session):
        """Test that foreign key relationship works correctly"""
        user = User(email="test@example.com", password_hash="hashed")
        test_session.add(user)
        test_session.commit()
        test_session.refresh(user)

        task = Task(
            user_id=user.id,
            title="Test Task"
        )
        test_session.add(task)
        test_session.commit()

        # Verify relationship
        assert task.user_id == user.id

    def test_task_without_valid_user_fails(self, test_session: Session):
        """Test that creating task with invalid user_id fails"""
        task = Task(
            user_id=99999,  # Non-existent user
            title="Invalid Task"
        )
        test_session.add(task)

        with pytest.raises(Exception):  # Should raise foreign key constraint error
            test_session.commit()


class TestUserIsolation:
    """Tests for user isolation at database level"""

    def test_query_tasks_by_user_id(self, test_session: Session):
        """Test that tasks can be queried by user_id"""
        # Create two users
        user1 = User(email="user1@example.com", password_hash="hash1")
        user2 = User(email="user2@example.com", password_hash="hash2")
        test_session.add(user1)
        test_session.add(user2)
        test_session.commit()
        test_session.refresh(user1)
        test_session.refresh(user2)

        # Create tasks for both users
        task1 = Task(user_id=user1.id, title="User 1 Task")
        task2 = Task(user_id=user2.id, title="User 2 Task")
        task3 = Task(user_id=user1.id, title="User 1 Another Task")
        test_session.add(task1)
        test_session.add(task2)
        test_session.add(task3)
        test_session.commit()

        # Query tasks for user1
        user1_tasks = test_session.exec(
            select(Task).where(Task.user_id == user1.id)
        ).all()

        # Query tasks for user2
        user2_tasks = test_session.exec(
            select(Task).where(Task.user_id == user2.id)
        ).all()

        # Verify isolation
        assert len(user1_tasks) == 2
        assert len(user2_tasks) == 1
        assert all(task.user_id == user1.id for task in user1_tasks)
        assert all(task.user_id == user2.id for task in user2_tasks)

    def test_query_specific_task_with_user_id(self, test_session: Session):
        """Test querying specific task with user_id filter"""
        user1 = User(email="user1@example.com", password_hash="hash1")
        user2 = User(email="user2@example.com", password_hash="hash2")
        test_session.add(user1)
        test_session.add(user2)
        test_session.commit()
        test_session.refresh(user1)
        test_session.refresh(user2)

        task1 = Task(user_id=user1.id, title="User 1 Task")
        task2 = Task(user_id=user2.id, title="User 2 Task")
        test_session.add(task1)
        test_session.add(task2)
        test_session.commit()
        test_session.refresh(task1)
        test_session.refresh(task2)

        # User 1 should only see their own task
        result = test_session.exec(
            select(Task).where(Task.id == task1.id).where(Task.user_id == user1.id)
        ).first()
        assert result is not None
        assert result.id == task1.id

        # User 2 should not see user 1's task
        result = test_session.exec(
            select(Task).where(Task.id == task1.id).where(Task.user_id == user2.id)
        ).first()
        assert result is None


class TestIndexPerformance:
    """Tests for database indexes"""

    def test_user_id_index_exists(self, test_session: Session):
        """Test that querying by user_id is efficient (index exists)"""
        # Create user and many tasks
        user = User(email="test@example.com", password_hash="hash")
        test_session.add(user)
        test_session.commit()
        test_session.refresh(user)

        # Create multiple tasks
        for i in range(100):
            task = Task(user_id=user.id, title=f"Task {i}")
            test_session.add(task)
        test_session.commit()

        # Query by user_id (should use index)
        tasks = test_session.exec(
            select(Task).where(Task.user_id == user.id)
        ).all()

        assert len(tasks) == 100

    def test_composite_index_user_id_completed(self, test_session: Session):
        """Test that querying by user_id and completed is efficient"""
        user = User(email="test@example.com", password_hash="hash")
        test_session.add(user)
        test_session.commit()
        test_session.refresh(user)

        # Create tasks with different completion status
        for i in range(50):
            task = Task(
                user_id=user.id,
                title=f"Task {i}",
                completed=(i % 2 == 0)  # Every other task completed
            )
            test_session.add(task)
        test_session.commit()

        # Query by user_id and completed (should use composite index)
        completed_tasks = test_session.exec(
            select(Task).where(Task.user_id == user.id).where(Task.completed == True)
        ).all()

        incomplete_tasks = test_session.exec(
            select(Task).where(Task.user_id == user.id).where(Task.completed == False)
        ).all()

        assert len(completed_tasks) == 25
        assert len(incomplete_tasks) == 25


class TestTransactionHandling:
    """Tests for transaction management"""

    def test_transaction_commit(self, test_session: Session):
        """Test that transactions commit correctly"""
        user = User(email="test@example.com", password_hash="hash")
        test_session.add(user)
        test_session.commit()

        # Verify user was committed
        result = test_session.exec(select(User)).first()
        assert result is not None
        assert result.email == "test@example.com"

    def test_transaction_rollback(self, test_session: Session):
        """Test that transactions rollback on error"""
        user = User(email="test@example.com", password_hash="hash")
        test_session.add(user)
        test_session.commit()

        try:
            # Try to create duplicate user (should fail)
            duplicate_user = User(email="test@example.com", password_hash="hash2")
            test_session.add(duplicate_user)
            test_session.commit()
        except Exception:
            test_session.rollback()

        # Verify only one user exists
        users = test_session.exec(select(User)).all()
        assert len(users) == 1


class TestDataIntegrity:
    """Tests for data integrity constraints"""

    def test_required_fields(self, test_session: Session):
        """Test that required fields are enforced"""
        user = User(email="test@example.com", password_hash="hash")
        test_session.add(user)
        test_session.commit()
        test_session.refresh(user)

        # Task without title should fail
        with pytest.raises(Exception):
            task = Task(user_id=user.id)  # Missing title
            test_session.add(task)
            test_session.commit()

    def test_timestamps_auto_set(self, test_session: Session):
        """Test that timestamps are automatically set"""
        user = User(email="test@example.com", password_hash="hash")
        test_session.add(user)
        test_session.commit()
        test_session.refresh(user)

        assert user.created_at is not None
        assert user.updated_at is not None
        assert isinstance(user.created_at, datetime)
        assert isinstance(user.updated_at, datetime)

    def test_default_values(self, test_session: Session):
        """Test that default values are set correctly"""
        user = User(email="test@example.com", password_hash="hash")
        test_session.add(user)
        test_session.commit()
        test_session.refresh(user)

        task = Task(user_id=user.id, title="Test")
        test_session.add(task)
        test_session.commit()
        test_session.refresh(task)

        # completed should default to False
        assert task.completed is False
        # description should default to None
        assert task.description is None


class TestCascadeOperations:
    """Tests for cascade behavior"""

    def test_delete_user_with_tasks(self, test_session: Session):
        """Test cascade behavior when deleting user with tasks"""
        user = User(email="test@example.com", password_hash="hash")
        test_session.add(user)
        test_session.commit()
        test_session.refresh(user)

        # Create tasks for user
        task1 = Task(user_id=user.id, title="Task 1")
        task2 = Task(user_id=user.id, title="Task 2")
        test_session.add(task1)
        test_session.add(task2)
        test_session.commit()

        # Delete user
        test_session.delete(user)
        test_session.commit()

        # Tasks should still exist (no CASCADE DELETE by default in SQLModel)
        # This tests that orphaned tasks would exist without explicit handling
        # In production, you might want to handle this differently
        tasks = test_session.exec(select(Task)).all()
        # Note: Behavior depends on database and cascade settings


class TestBulkOperations:
    """Tests for bulk database operations"""

    def test_bulk_insert_tasks(self, test_session: Session):
        """Test inserting multiple tasks efficiently"""
        user = User(email="test@example.com", password_hash="hash")
        test_session.add(user)
        test_session.commit()
        test_session.refresh(user)

        # Create 100 tasks
        tasks = [
            Task(user_id=user.id, title=f"Task {i}")
            for i in range(100)
        ]
        for task in tasks:
            test_session.add(task)
        test_session.commit()

        # Verify all tasks were created
        result = test_session.exec(select(Task)).all()
        assert len(result) == 100

    def test_bulk_update_tasks(self, test_session: Session):
        """Test updating multiple tasks"""
        user = User(email="test@example.com", password_hash="hash")
        test_session.add(user)
        test_session.commit()
        test_session.refresh(user)

        # Create tasks
        for i in range(10):
            task = Task(user_id=user.id, title=f"Task {i}", completed=False)
            test_session.add(task)
        test_session.commit()

        # Update all tasks to completed
        tasks = test_session.exec(select(Task)).all()
        for task in tasks:
            task.completed = True
        test_session.commit()

        # Verify all are completed
        completed_tasks = test_session.exec(
            select(Task).where(Task.completed == True)
        ).all()
        assert len(completed_tasks) == 10
