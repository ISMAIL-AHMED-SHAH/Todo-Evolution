"""
Backend Implementation Skills

Skills for generating and working with FastAPI + SQLModel backend code.
"""

from typing import Dict, Any, List, Optional
from pathlib import Path


class BackendSkills:
    """Skills for FastAPI + SQLModel backend implementation."""

    def __init__(self, backend_root: Optional[Path] = None):
        """
        Initialize backend skills.

        Args:
            backend_root: Root directory for backend code (defaults to ./backend)
        """
        self.backend_root = backend_root or Path("backend")

    def generate_fastapi_routes(
        self,
        resource: str,
        endpoints: List[Dict[str, str]]
    ) -> str:
        """
        Generate FastAPI route definitions.

        Args:
            resource: Resource name (e.g., "tasks")
            endpoints: List of endpoint definitions

        Returns:
            Generated FastAPI code

        Example:
            >>> skills = BackendSkills()
            >>> code = skills.generate_fastapi_routes("tasks", [
            ...     {"method": "GET", "path": "/api/{user_id}/tasks"}
            ... ])
        """
        code_lines = [
            '"""',
            f'{resource.capitalize()} API Routes',
            '"""',
            '',
            'from fastapi import APIRouter, Depends, HTTPException, status',
            'from sqlmodel import Session',
            'from typing import List',
            '',
            'from ..models import Task, TaskCreate, TaskUpdate',
            'from ..services.task_service import TaskService',
            'from ..auth.dependencies import get_current_user, get_db',
            '',
            f'router = APIRouter(prefix="/api", tags=["{resource}"])',
            ''
        ]

        for endpoint in endpoints:
            method = endpoint["method"].lower()
            path = endpoint["path"]

            # Generate route handler
            handler_name = self._generate_handler_name(method, path)
            code_lines.extend(self._generate_route_handler(method, path, handler_name))
            code_lines.append('')

        return '\n'.join(code_lines)

    def generate_models_sqlmodel(
        self,
        entity_name: str,
        fields: Dict[str, str]
    ) -> str:
        """
        Generate SQLModel entity definitions.

        Args:
            entity_name: Name of the entity (e.g., "Task")
            fields: Dictionary of field_name: field_type

        Returns:
            Generated SQLModel code

        Example:
            >>> skills = BackendSkills()
            >>> code = skills.generate_models_sqlmodel("Task", {
            ...     "title": "str",
            ...     "completed": "bool"
            ... })
        """
        code_lines = [
            '"""',
            f'{entity_name} Entity Model',
            '"""',
            '',
            'from sqlmodel import SQLModel, Field',
            'from typing import Optional',
            'from datetime import datetime',
            '',
            f'class {entity_name}Base(SQLModel):',
            '    """Base model for shared fields."""'
        ]

        # Add base fields
        for field_name, field_type in fields.items():
            if field_name not in ['id', 'created_at', 'updated_at']:
                code_lines.append(f'    {field_name}: {field_type}')

        code_lines.extend([
            '',
            f'class {entity_name}(SQLModel, table=True):',
            f'    """Database model for {entity_name}."""',
            '    id: Optional[int] = Field(default=None, primary_key=True)',
        ])

        # Add all fields
        for field_name, field_type in fields.items():
            if field_name != 'id':
                code_lines.append(f'    {field_name}: {field_type}')

        code_lines.extend([
            '    created_at: datetime = Field(default_factory=datetime.utcnow)',
            '    updated_at: datetime = Field(default_factory=datetime.utcnow)',
            '',
            f'class {entity_name}Create({entity_name}Base):',
            f'    """Model for creating {entity_name}."""',
            '    pass',
            '',
            f'class {entity_name}Update(SQLModel):',
            f'    """Model for updating {entity_name}."""'
        ])

        # Add optional update fields
        for field_name, field_type in fields.items():
            if field_name not in ['id', 'created_at', 'updated_at']:
                code_lines.append(f'    {field_name}: Optional[{field_type}] = None')

        return '\n'.join(code_lines)

    def apply_migrations(self, migration_name: str) -> Dict[str, Any]:
        """
        Generate migration file template.

        Args:
            migration_name: Name of the migration

        Returns:
            Migration file content and metadata
        """
        return {
            "migration_name": migration_name,
            "content": self._generate_migration_template(migration_name),
            "path": f"backend/alembic/versions/{migration_name}.py"
        }

    def create_db_connection(self) -> str:
        """
        Generate database connection setup code.

        Returns:
            Database connection code
        """
        return '''"""
Database Connection Setup
"""

from sqlmodel import create_engine, Session
from typing import Generator
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://user:password@localhost:5432/todo_db"
)

engine = create_engine(DATABASE_URL, echo=True)


def get_db() -> Generator[Session, None, None]:
    """Get database session."""
    with Session(engine) as session:
        yield session
'''

    def implement_rest_endpoints(
        self,
        resource: str,
        operations: List[str]
    ) -> Dict[str, str]:
        """
        Implement REST endpoint handlers.

        Args:
            resource: Resource name
            operations: List of operations (e.g., ["create", "read", "update", "delete"])

        Returns:
            Dictionary of operation: code
        """
        implementations = {}

        for operation in operations:
            implementations[operation] = self._generate_operation_code(resource, operation)

        return implementations

    def enforce_jwt_security(self) -> str:
        """
        Generate JWT security middleware code.

        Returns:
            JWT middleware code
        """
        return '''"""
JWT Authentication Middleware
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    """
    Verify JWT token and extract user information.

    Args:
        credentials: HTTP Authorization credentials

    Returns:
        User information from token

    Raises:
        HTTPException: If token is invalid or expired
    """
    token = credentials.credentials

    # TODO: Implement JWT verification using JWTHelper
    # from intelligence.tools import JWTHelper
    # jwt_helper = JWTHelper()
    # payload = jwt_helper.verify_token(token)

    # if not payload:
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Invalid or expired token"
    #     )

    # return payload

    raise NotImplementedError("JWT verification not implemented")


async def verify_user_ownership(
    user_id: int,
    current_user: dict = Depends(get_current_user)
) -> bool:
    """
    Verify that the current user owns the resource.

    Args:
        user_id: User ID from URL path
        current_user: Current authenticated user

    Returns:
        True if user owns resource

    Raises:
        HTTPException: If user doesn't own resource
    """
    if current_user.get("user_id") != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: You can only access your own resources"
        )

    return True
'''

    def _generate_handler_name(self, method: str, path: str) -> str:
        """Generate handler function name from method and path."""
        # Extract meaningful parts from path
        parts = [p for p in path.split('/') if p and not p.startswith('{')]

        if method == 'get' and '{id}' in path:
            return f"get_{parts[-1]}_by_id"
        elif method == 'get':
            return f"list_{parts[-1]}"
        elif method == 'post':
            return f"create_{parts[-1][:-1]}"  # Remove plural 's'
        elif method == 'put':
            return f"update_{parts[-1][:-1]}"
        elif method == 'delete':
            return f"delete_{parts[-1][:-1]}"
        elif method == 'patch':
            return f"patch_{parts[-1][:-1]}"

        return f"{method}_{parts[-1]}"

    def _generate_route_handler(
        self,
        method: str,
        path: str,
        handler_name: str
    ) -> List[str]:
        """Generate route handler code."""
        # Simplify path for FastAPI (remove /api prefix if present)
        fastapi_path = path.replace('/api', '', 1)

        return [
            f'@router.{method}("{fastapi_path}")',
            f'async def {handler_name}(',
            '    user_id: int,',
            '    current_user: dict = Depends(get_current_user),',
            '    db: Session = Depends(get_db)',
            '):',
            '    """TODO: Implement endpoint logic."""',
            '    # Verify user ownership',
            '    if current_user.get("user_id") != user_id:',
            '        raise HTTPException(status_code=403, detail="Access denied")',
            '    ',
            '    # TODO: Implement logic',
            '    raise NotImplementedError("Endpoint not implemented")'
        ]

    def _generate_migration_template(self, name: str) -> str:
        """Generate Alembic migration template."""
        return f'''"""
{name}

Revision ID: <generated>
"""

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers
revision = '<generated>'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Upgrade database schema."""
    # TODO: Add migration logic
    pass


def downgrade() -> None:
    """Downgrade database schema."""
    # TODO: Add rollback logic
    pass
'''

    def _generate_operation_code(self, resource: str, operation: str) -> str:
        """Generate code for a specific operation."""
        templates = {
            "create": f'''
async def create_{resource}(
    user_id: int,
    item: {resource.capitalize()}Create,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Create a new {resource}."""
    # Verify ownership
    if current_user.get("user_id") != user_id:
        raise HTTPException(status_code=403, detail="Access denied")

    # Create item with user_id
    db_item = {resource.capitalize()}(**item.dict(), user_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    return db_item
''',
            "read": f'''
async def get_{resource}(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get all {resource} for user."""
    # Verify ownership
    if current_user.get("user_id") != user_id:
        raise HTTPException(status_code=403, detail="Access denied")

    items = db.query({resource.capitalize()}).filter_by(user_id=user_id).all()
    return items
''',
        }

        return templates.get(operation, "# TODO: Implement operation")
