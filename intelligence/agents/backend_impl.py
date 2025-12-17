"""
Backend Implementation Agent

Agent specialized in FastAPI + SQLModel backend code generation and implementation.
"""

from typing import Dict, Any, List, Optional
from pathlib import Path
from .base import BaseAgent
from ..skills import BackendSkills


class BackendImplementationAgent(BaseAgent):
    """Agent for FastAPI + SQLModel backend implementation."""

    def __init__(self, backend_root: Optional[Path] = None):
        """
        Initialize Backend Implementation Agent.

        Args:
            backend_root: Root directory for backend code
        """
        super().__init__(
            name="Backend-Implementation-Agent",
            description="Generates FastAPI routes, SQLModel models, and backend infrastructure"
        )
        self.skills = BackendSkills(backend_root)

    def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a backend implementation task.

        Args:
            task: Task specification with 'skill' and 'params'

        Returns:
            Task result
        """
        skill = task.get("skill")
        params = task.get("params", {})

        if skill == "generate_fastapi_routes":
            result = {"code": self.skills.generate_fastapi_routes(**params)}

        elif skill == "generate_models_sqlmodel":
            result = {"code": self.skills.generate_models_sqlmodel(**params)}

        elif skill == "apply_migrations":
            result = self.skills.apply_migrations(**params)

        elif skill == "create_db_connection":
            result = {"code": self.skills.create_db_connection()}

        elif skill == "implement_rest_endpoints":
            result = {"implementations": self.skills.implement_rest_endpoints(**params)}

        elif skill == "enforce_jwt_security":
            result = {"code": self.skills.enforce_jwt_security()}

        else:
            result = {
                "error": f"Unknown skill: {skill}",
                "available_skills": self._list_skills()
            }

        self.log_execution(task, result)
        return result

    def generate_fastapi_routes(
        self,
        resource: str,
        endpoints: List[Dict[str, str]]
    ) -> str:
        """
        Generate FastAPI routes.

        Args:
            resource: Resource name
            endpoints: List of endpoint definitions

        Returns:
            Generated code
        """
        result = self.execute({
            "skill": "generate_fastapi_routes",
            "params": {"resource": resource, "endpoints": endpoints}
        })
        return result.get("code", "")

    def generate_models_sqlmodel(
        self,
        entity_name: str,
        fields: Dict[str, str]
    ) -> str:
        """
        Generate SQLModel entities.

        Args:
            entity_name: Entity name
            fields: Field definitions

        Returns:
            Generated code
        """
        result = self.execute({
            "skill": "generate_models_sqlmodel",
            "params": {"entity_name": entity_name, "fields": fields}
        })
        return result.get("code", "")

    def create_db_connection(self) -> str:
        """
        Generate database connection code.

        Returns:
            Database connection code
        """
        result = self.execute({
            "skill": "create_db_connection",
            "params": {}
        })
        return result.get("code", "")

    def implement_rest_endpoints(
        self,
        resource: str,
        operations: List[str]
    ) -> Dict[str, str]:
        """
        Implement REST endpoints.

        Args:
            resource: Resource name
            operations: List of operations

        Returns:
            Dictionary of operation: code
        """
        result = self.execute({
            "skill": "implement_rest_endpoints",
            "params": {"resource": resource, "operations": operations}
        })
        return result.get("implementations", {})

    def enforce_jwt_security(self) -> str:
        """
        Generate JWT security middleware.

        Returns:
            Middleware code
        """
        result = self.execute({
            "skill": "enforce_jwt_security",
            "params": {}
        })
        return result.get("code", "")

    def _list_skills(self) -> List[str]:
        """List available skills."""
        return [
            "generate_fastapi_routes",
            "generate_models_sqlmodel",
            "apply_migrations",
            "create_db_connection",
            "implement_rest_endpoints",
            "enforce_jwt_security"
        ]
