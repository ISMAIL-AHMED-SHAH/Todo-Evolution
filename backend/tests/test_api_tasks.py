"""
Comprehensive API tests for task endpoints

Tests cover:
- All CRUD operations
- User isolation enforcement
- Authentication requirements
- Proper status codes
- Error handling
"""
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine, SQLModel
from sqlmodel.pool import StaticPool

from src.main import app
from src.database import get_session
from src.models.user import User
from src.models.task import Task
from src.auth import create_access_token


# Setup test database
@pytest.fixture(name="session")
def session_fixture():
    """Create a fresh database session for each test"""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    """Create a test client with overridden database session"""
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture(name="test_user")
def test_user_fixture(session: Session):
    """Create a test user"""
    user = User(
        email="test@example.com",
        password_hash="hashed_password_here"  # In real scenario, properly hash
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@pytest.fixture(name="test_user2")
def test_user2_fixture(session: Session):
    """Create a second test user for isolation testing"""
    user = User(
        email="test2@example.com",
        password_hash="hashed_password_here"
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@pytest.fixture(name="auth_token")
def auth_token_fixture(test_user: User):
    """Generate authentication token for test user"""
    token = create_access_token({"sub": str(test_user.id)})
    return token


@pytest.fixture(name="auth_headers")
def auth_headers_fixture(auth_token: str):
    """Create headers with authentication token"""
    return {"Authorization": f"Bearer {auth_token}"}


class TestGetTasks:
    """Tests for GET /{user_id}/tasks endpoint"""

    def test_get_tasks_success(self, client: TestClient, test_user: User, auth_headers: dict, session: Session):
        """Test successfully getting all tasks for a user"""
        # Create some test tasks
        task1 = Task(user_id=test_user.id, title="Task 1", description="Description 1")
        task2 = Task(user_id=test_user.id, title="Task 2", completed=True)
        session.add(task1)
        session.add(task2)
        session.commit()

        # Get tasks
        response = client.get(f"/{test_user.id}/tasks", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["title"] == "Task 1"
        assert data[1]["title"] == "Task 2"
        assert data[1]["completed"] is True

    def test_get_tasks_empty(self, client: TestClient, test_user: User, auth_headers: dict):
        """Test getting tasks when none exist"""
        response = client.get(f"/{test_user.id}/tasks", headers=auth_headers)

        assert response.status_code == 200
        assert response.json() == []

    def test_get_tasks_unauthorized(self, client: TestClient, test_user: User):
        """Test getting tasks without authentication"""
        response = client.get(f"/{test_user.id}/tasks")

        assert response.status_code == 401

    def test_get_tasks_forbidden_other_user(self, client: TestClient, test_user: User, test_user2: User, auth_headers: dict):
        """Test that users cannot access other users' tasks"""
        response = client.get(f"/{test_user2.id}/tasks", headers=auth_headers)

        assert response.status_code == 403
        assert "only access your own tasks" in response.json()["detail"]


class TestCreateTask:
    """Tests for POST /{user_id}/tasks endpoint"""

    def test_create_task_success(self, client: TestClient, test_user: User, auth_headers: dict):
        """Test successfully creating a task"""
        task_data = {
            "title": "New Task",
            "description": "Task description"
        }

        response = client.post(f"/{test_user.id}/tasks", json=task_data, headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "New Task"
        assert data["description"] == "Task description"
        assert data["completed"] is False
        assert "id" in data
        assert data["user_id"] == test_user.id

    def test_create_task_minimal(self, client: TestClient, test_user: User, auth_headers: dict):
        """Test creating a task with only required fields"""
        task_data = {"title": "Minimal Task"}

        response = client.post(f"/{test_user.id}/tasks", json=task_data, headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Minimal Task"
        assert data["description"] is None

    def test_create_task_missing_title(self, client: TestClient, test_user: User, auth_headers: dict):
        """Test creating a task without required title"""
        task_data = {"description": "No title"}

        response = client.post(f"/{test_user.id}/tasks", json=task_data, headers=auth_headers)

        assert response.status_code == 422  # Validation error

    def test_create_task_unauthorized(self, client: TestClient, test_user: User):
        """Test creating a task without authentication"""
        task_data = {"title": "Unauthorized"}

        response = client.post(f"/{test_user.id}/tasks", json=task_data)

        assert response.status_code == 401

    def test_create_task_for_other_user(self, client: TestClient, test_user: User, test_user2: User, auth_headers: dict):
        """Test that users cannot create tasks for other users"""
        task_data = {"title": "Other user task"}

        response = client.post(f"/{test_user2.id}/tasks", json=task_data, headers=auth_headers)

        assert response.status_code == 403


class TestGetSingleTask:
    """Tests for GET /{user_id}/tasks/{id} endpoint"""

    def test_get_task_success(self, client: TestClient, test_user: User, auth_headers: dict, session: Session):
        """Test successfully getting a specific task"""
        task = Task(user_id=test_user.id, title="Specific Task")
        session.add(task)
        session.commit()
        session.refresh(task)

        response = client.get(f"/{test_user.id}/tasks/{task.id}", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == task.id
        assert data["title"] == "Specific Task"

    def test_get_task_not_found(self, client: TestClient, test_user: User, auth_headers: dict):
        """Test getting a non-existent task"""
        response = client.get(f"/{test_user.id}/tasks/99999", headers=auth_headers)

        assert response.status_code == 404

    def test_get_task_other_user(self, client: TestClient, test_user: User, test_user2: User, auth_headers: dict, session: Session):
        """Test that users cannot access other users' tasks"""
        # Create task for user2
        task = Task(user_id=test_user2.id, title="User 2 Task")
        session.add(task)
        session.commit()

        # Try to access with user1's token
        response = client.get(f"/{test_user2.id}/tasks/{task.id}", headers=auth_headers)

        assert response.status_code == 403


class TestUpdateTask:
    """Tests for PUT /{user_id}/tasks/{id} endpoint"""

    def test_update_task_success(self, client: TestClient, test_user: User, auth_headers: dict, session: Session):
        """Test successfully updating a task"""
        task = Task(user_id=test_user.id, title="Original Title")
        session.add(task)
        session.commit()
        session.refresh(task)

        update_data = {
            "title": "Updated Title",
            "description": "New description",
            "completed": True
        }

        response = client.put(f"/{test_user.id}/tasks/{task.id}", json=update_data, headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Title"
        assert data["description"] == "New description"
        assert data["completed"] is True

    def test_update_task_partial(self, client: TestClient, test_user: User, auth_headers: dict, session: Session):
        """Test partially updating a task"""
        task = Task(user_id=test_user.id, title="Original", description="Original desc")
        session.add(task)
        session.commit()
        session.refresh(task)

        update_data = {"title": "Updated Only Title"}

        response = client.put(f"/{test_user.id}/tasks/{task.id}", json=update_data, headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Only Title"
        assert data["description"] == "Original desc"  # Should remain unchanged

    def test_update_task_not_found(self, client: TestClient, test_user: User, auth_headers: dict):
        """Test updating a non-existent task"""
        update_data = {"title": "Update"}

        response = client.put(f"/{test_user.id}/tasks/99999", json=update_data, headers=auth_headers)

        assert response.status_code == 404


class TestDeleteTask:
    """Tests for DELETE /{user_id}/tasks/{id} endpoint"""

    def test_delete_task_success(self, client: TestClient, test_user: User, auth_headers: dict, session: Session):
        """Test successfully deleting a task"""
        task = Task(user_id=test_user.id, title="To Delete")
        session.add(task)
        session.commit()
        session.refresh(task)
        task_id = task.id

        response = client.delete(f"/{test_user.id}/tasks/{task_id}", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == task_id
        assert data["title"] == "To Delete"

        # Verify task is actually deleted
        get_response = client.get(f"/{test_user.id}/tasks/{task_id}", headers=auth_headers)
        assert get_response.status_code == 404

    def test_delete_task_not_found(self, client: TestClient, test_user: User, auth_headers: dict):
        """Test deleting a non-existent task"""
        response = client.delete(f"/{test_user.id}/tasks/99999", headers=auth_headers)

        assert response.status_code == 404


class TestUpdateTaskCompletion:
    """Tests for PATCH /{user_id}/tasks/{id}/complete endpoint"""

    def test_mark_task_complete(self, client: TestClient, test_user: User, auth_headers: dict, session: Session):
        """Test marking a task as complete"""
        task = Task(user_id=test_user.id, title="To Complete", completed=False)
        session.add(task)
        session.commit()
        session.refresh(task)

        response = client.patch(
            f"/{test_user.id}/tasks/{task.id}/complete",
            json={"completed": True},
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert data["completed"] is True

    def test_mark_task_incomplete(self, client: TestClient, test_user: User, auth_headers: dict, session: Session):
        """Test marking a task as incomplete"""
        task = Task(user_id=test_user.id, title="To Uncomplete", completed=True)
        session.add(task)
        session.commit()
        session.refresh(task)

        response = client.patch(
            f"/{test_user.id}/tasks/{task.id}/complete",
            json={"completed": False},
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert data["completed"] is False

    def test_update_completion_not_found(self, client: TestClient, test_user: User, auth_headers: dict):
        """Test updating completion status of non-existent task"""
        response = client.patch(
            f"/{test_user.id}/tasks/99999/complete",
            json={"completed": True},
            headers=auth_headers
        )

        assert response.status_code == 404


class TestUserIsolation:
    """Integration tests for user isolation enforcement"""

    def test_complete_isolation(self, client: TestClient, test_user: User, test_user2: User, auth_headers: dict, session: Session):
        """Test that user isolation is enforced across all endpoints"""
        # Create tasks for both users
        task1 = Task(user_id=test_user.id, title="User 1 Task")
        task2 = Task(user_id=test_user2.id, title="User 2 Task")
        session.add(task1)
        session.add(task2)
        session.commit()

        # User 1 should only see their own tasks
        response = client.get(f"/{test_user.id}/tasks", headers=auth_headers)
        assert response.status_code == 200
        tasks = response.json()
        assert len(tasks) == 1
        assert tasks[0]["title"] == "User 1 Task"

        # User 1 cannot access User 2's tasks
        response = client.get(f"/{test_user2.id}/tasks/{task2.id}", headers=auth_headers)
        assert response.status_code == 403
