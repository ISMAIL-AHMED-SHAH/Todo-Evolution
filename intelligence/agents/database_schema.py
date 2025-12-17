"""
Database Schema Agent

Agent specialized in SQLModel schema management and PostgreSQL operations.
"""

from typing import Dict, Any, List
from .base import BaseAgent
from ..skills import DatabaseSkills


class DatabaseSchemaAgent(BaseAgent):
    """Agent for database schema and migration management."""

    def __init__(self):
        """Initialize Database Schema Agent."""
        super().__init__(
            name="Database-Schema-Agent",
            description="Manages SQLModel schemas, migrations, and database operations"
        )
        self.skills = DatabaseSkills()

    def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a database schema task.

        Args:
            task: Task specification with 'skill' and 'params'

        Returns:
            Task result
        """
        skill = task.get("skill")
        params = task.get("params", {})

        if skill == "evolve_schema":
            result = self.skills.evolve_schema(**params)

        elif skill == "update_tasks_table":
            result = {"code": self.skills.update_tasks_table(**params)}

        elif skill == "generate_migrations":
            result = {"migrations": self.skills.generate_migrations(**params)}

        elif skill == "create_indexes":
            result = {"code": self.skills.create_indexes(**params)}

        elif skill == "setup_foreign_keys":
            result = {"code": self.skills.setup_foreign_keys(**params)}

        else:
            result = {
                "error": f"Unknown skill: {skill}",
                "available_skills": self._list_skills()
            }

        self.log_execution(task, result)
        return result

    def evolve_schema(self, changes: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate schema evolution migration.

        Args:
            changes: List of schema changes

        Returns:
            Migration information
        """
        return self.execute({
            "skill": "evolve_schema",
            "params": {"changes": changes}
        })

    def update_tasks_table(self, new_fields: Dict[str, str]) -> str:
        """
        Generate migration to update tasks table.

        Args:
            new_fields: Dictionary of field_name: field_type

        Returns:
            Migration code
        """
        result = self.execute({
            "skill": "update_tasks_table",
            "params": {"new_fields": new_fields}
        })
        return result.get("code", "")

    def generate_migrations(self, entities: List[Dict[str, Any]]) -> Dict[str, str]:
        """
        Generate initial migrations.

        Args:
            entities: List of entity definitions

        Returns:
            Dictionary of migration_name: code
        """
        result = self.execute({
            "skill": "generate_migrations",
            "params": {"entities": entities}
        })
        return result.get("migrations", {})

    def create_indexes(
        self,
        table: str,
        indexes: List[Dict[str, Any]]
    ) -> str:
        """
        Generate index creation migration.

        Args:
            table: Table name
            indexes: List of index definitions

        Returns:
            Migration code
        """
        result = self.execute({
            "skill": "create_indexes",
            "params": {"table": table, "indexes": indexes}
        })
        return result.get("code", "")

    def setup_foreign_keys(self, relationships: List[Dict[str, str]]) -> str:
        """
        Generate foreign key migration.

        Args:
            relationships: List of foreign key relationships

        Returns:
            Migration code
        """
        result = self.execute({
            "skill": "setup_foreign_keys",
            "params": {"relationships": relationships}
        })
        return result.get("code", "")

    def _list_skills(self) -> List[str]:
        """List available skills."""
        return [
            "evolve_schema",
            "update_tasks_table",
            "generate_migrations",
            "create_indexes",
            "setup_foreign_keys"
        ]
