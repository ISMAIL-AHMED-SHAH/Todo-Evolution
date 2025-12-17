"""
Frontend Implementation Agent

Agent specialized in Next.js + Better Auth frontend code generation.
"""

from typing import Dict, Any, List, Optional
from pathlib import Path
from .base import BaseAgent
from ..skills import FrontendSkills


class FrontendImplementationAgent(BaseAgent):
    """Agent for Next.js + Better Auth frontend implementation."""

    def __init__(self, frontend_root: Optional[Path] = None):
        """
        Initialize Frontend Implementation Agent.

        Args:
            frontend_root: Root directory for frontend code
        """
        super().__init__(
            name="Frontend-Implementation-Agent",
            description="Generates Next.js pages, components, and API client integration"
        )
        self.skills = FrontendSkills(frontend_root)

    def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a frontend implementation task.

        Args:
            task: Task specification with 'skill' and 'params'

        Returns:
            Task result
        """
        skill = task.get("skill")
        params = task.get("params", {})

        if skill == "generate_nextjs_routes":
            result = {"pages": self.skills.generate_nextjs_routes(**params)}

        elif skill == "auth_ui_components":
            result = {"components": self.skills.auth_ui_components()}

        elif skill == "create_frontend_api_client":
            result = {"code": self.skills.create_frontend_api_client(**params)}

        elif skill == "connect_to_fastapi_api":
            result = {"code": self.skills.connect_to_fastapi_api(**params)}

        else:
            result = {
                "error": f"Unknown skill: {skill}",
                "available_skills": self._list_skills()
            }

        self.log_execution(task, result)
        return result

    def generate_nextjs_routes(
        self,
        pages: List[Dict[str, str]]
    ) -> Dict[str, str]:
        """
        Generate Next.js page routes.

        Args:
            pages: List of page definitions

        Returns:
            Dictionary of filename: code
        """
        result = self.execute({
            "skill": "generate_nextjs_routes",
            "params": {"pages": pages}
        })
        return result.get("pages", {})

    def auth_ui_components(self) -> Dict[str, str]:
        """
        Generate authentication UI components.

        Returns:
            Dictionary of component_name: code
        """
        result = self.execute({
            "skill": "auth_ui_components",
            "params": {}
        })
        return result.get("components", {})

    def create_frontend_api_client(self, base_url: str = "http://localhost:8000") -> str:
        """
        Generate frontend API client.

        Args:
            base_url: Backend API base URL

        Returns:
            API client code
        """
        result = self.execute({
            "skill": "create_frontend_api_client",
            "params": {"base_url": base_url}
        })
        return result.get("code", "")

    def connect_to_fastapi_api(self, endpoints: List[Dict[str, str]]) -> str:
        """
        Generate TypeScript service for FastAPI endpoints.

        Args:
            endpoints: List of endpoint definitions

        Returns:
            TypeScript service code
        """
        result = self.execute({
            "skill": "connect_to_fastapi_api",
            "params": {"endpoints": endpoints}
        })
        return result.get("code", "")

    def _list_skills(self) -> List[str]:
        """List available skills."""
        return [
            "generate_nextjs_routes",
            "auth_ui_components",
            "create_frontend_api_client",
            "connect_to_fastapi_api"
        ]
