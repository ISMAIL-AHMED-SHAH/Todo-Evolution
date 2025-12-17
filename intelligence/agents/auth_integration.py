"""
Auth Integration Agent

Agent specialized in JWT and Better Auth configuration and integration.
"""

from typing import Dict, Any, List
from .base import BaseAgent
from ..skills import AuthSkills


class AuthIntegrationAgent(BaseAgent):
    """Agent for JWT and Better Auth integration."""

    def __init__(self):
        """Initialize Auth Integration Agent."""
        super().__init__(
            name="Auth-Integration-Agent",
            description="Configures Better Auth, JWT verification, and user isolation enforcement"
        )
        self.skills = AuthSkills()

    def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute an authentication integration task.

        Args:
            task: Task specification with 'skill' and 'params'

        Returns:
            Task result
        """
        skill = task.get("skill")
        params = task.get("params", {})

        if skill == "configure_better_auth_jwt":
            result = {"config_files": self.skills.configure_better_auth_jwt()}

        elif skill == "jwt_verification_middleware":
            result = {"code": self.skills.jwt_verification_middleware()}

        elif skill == "sync_frontend_backend_auth":
            result = {"components": self.skills.sync_frontend_backend_auth()}

        elif skill == "enforce_user_isolation":
            result = {"code": self.skills.enforce_user_isolation()}

        else:
            result = {
                "error": f"Unknown skill: {skill}",
                "available_skills": self._list_skills()
            }

        self.log_execution(task, result)
        return result

    def configure_better_auth_jwt(self) -> Dict[str, str]:
        """
        Generate Better Auth configuration.

        Returns:
            Dictionary of config_file: code
        """
        result = self.execute({
            "skill": "configure_better_auth_jwt",
            "params": {}
        })
        return result.get("config_files", {})

    def jwt_verification_middleware(self) -> str:
        """
        Generate JWT verification middleware.

        Returns:
            Middleware code
        """
        result = self.execute({
            "skill": "jwt_verification_middleware",
            "params": {}
        })
        return result.get("code", "")

    def sync_frontend_backend_auth(self) -> Dict[str, str]:
        """
        Generate auth sync components.

        Returns:
            Dictionary of component_name: code
        """
        result = self.execute({
            "skill": "sync_frontend_backend_auth",
            "params": {}
        })
        return result.get("components", {})

    def enforce_user_isolation(self) -> str:
        """
        Generate user isolation decorator.

        Returns:
            Decorator code
        """
        result = self.execute({
            "skill": "enforce_user_isolation",
            "params": {}
        })
        return result.get("code", "")

    def _list_skills(self) -> List[str]:
        """List available skills."""
        return [
            "configure_better_auth_jwt",
            "jwt_verification_middleware",
            "sync_frontend_backend_auth",
            "enforce_user_isolation"
        ]
