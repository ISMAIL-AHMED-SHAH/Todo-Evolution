"""
Database Schema Skills

Skills for working with SQLModel and PostgreSQL database operations.
"""

from typing import Dict, Any, List, Optional
from pathlib import Path


class DatabaseSkills:
    """Skills for database schema and migration management."""

    def __init__(self):
        """Initialize database skills."""
        pass

    def evolve_schema(
        self,
        changes: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Generate schema evolution migration.

        Args:
            changes: List of schema changes

        Returns:
            Migration file information

        Example:
            >>> skills = DatabaseSkills()
            >>> migration = skills.evolve_schema([
            ...     {"action": "add_column", "table": "tasks", "column": "priority"}
            ... ])
        """
        migration_name = "evolve_schema_" + "_".join(
            [change.get("action", "change") for change in changes[:2]]
        )

        migration_code = self._generate_evolution_migration(changes)

        return {
            "name": migration_name,
            "code": migration_code,
            "path": f"backend/alembic/versions/{migration_name}.py"
        }

    def update_tasks_table(self, new_fields: Dict[str, str]) -> str:
        """
        Generate migration to update tasks table.

        Args:
            new_fields: Dictionary of field_name: field_type

        Returns:
            Migration code

        Example:
            >>> skills = DatabaseSkills()
            >>> migration = skills.update_tasks_table({"priority": "Integer"})
        """
        return self._generate_table_update_migration("tasks", new_fields)

    def generate_migrations(
        self,
        entities: List[Dict[str, Any]]
    ) -> Dict[str, str]:
        """
        Generate initial migrations for entities.

        Args:
            entities: List of entity definitions

        Returns:
            Dictionary of migration_name: code

        Example:
            >>> skills = DatabaseSkills()
            >>> migrations = skills.generate_migrations([
            ...     {"name": "User", "fields": {"email": "String"}},
            ...     {"name": "Task", "fields": {"title": "String"}}
            ... ])
        """
        migrations = {}

        for entity in entities:
            migration_name = f"create_{entity['name'].lower()}_table"
            migration_code = self._generate_create_table_migration(entity)

            migrations[migration_name] = migration_code

        return migrations

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

        Example:
            >>> skills = DatabaseSkills()
            >>> migration = skills.create_indexes("tasks", [
            ...     {"columns": ["user_id"], "name": "idx_tasks_user_id"}
            ... ])
        """
        return self._generate_index_migration(table, indexes)

    def setup_foreign_keys(
        self,
        relationships: List[Dict[str, str]]
    ) -> str:
        """
        Generate foreign key constraints migration.

        Args:
            relationships: List of foreign key relationships

        Returns:
            Migration code

        Example:
            >>> skills = DatabaseSkills()
            >>> migration = skills.setup_foreign_keys([
            ...     {"from_table": "tasks", "from_column": "user_id",
            ...      "to_table": "users", "to_column": "id"}
            ... ])
        """
        return self._generate_foreign_key_migration(relationships)

    def _generate_evolution_migration(self, changes: List[Dict[str, Any]]) -> str:
        """Generate migration code for schema evolution."""
        operations = []

        for change in changes:
            action = change.get("action")

            if action == "add_column":
                operations.append(
                    f"    op.add_column('{change['table']}', "
                    f"sa.Column('{change['column']}', sa.{change.get('type', 'String')}()))"
                )
            elif action == "drop_column":
                operations.append(
                    f"    op.drop_column('{change['table']}', '{change['column']}')"
                )
            elif action == "alter_column":
                operations.append(
                    f"    op.alter_column('{change['table']}', '{change['column']}', "
                    f"type_=sa.{change.get('new_type', 'String')}())"
                )

        upgrade_ops = "\n".join(operations)
        downgrade_ops = "    pass  # TODO: Implement rollback"

        return f'''"""
Schema evolution migration

Revision ID: <generated>
"""

from alembic import op
import sqlalchemy as sa


revision = '<generated>'
down_revision = None


def upgrade() -> None:
    """Apply schema changes."""
{upgrade_ops}


def downgrade() -> None:
    """Rollback schema changes."""
{downgrade_ops}
'''

    def _generate_table_update_migration(
        self,
        table: str,
        new_fields: Dict[str, str]
    ) -> str:
        """Generate migration to update a table."""
        operations = []

        for field_name, field_type in new_fields.items():
            operations.append(
                f"    op.add_column('{table}', "
                f"sa.Column('{field_name}', sa.{field_type}()))"
            )

        upgrade_ops = "\n".join(operations)

        return f'''"""
Update {table} table

Revision ID: <generated>
"""

from alembic import op
import sqlalchemy as sa


revision = '<generated>'
down_revision = None


def upgrade() -> None:
    """Add new columns to {table}."""
{upgrade_ops}


def downgrade() -> None:
    """Remove columns from {table}."""
    # Reverse operations
{self._generate_reverse_operations(new_fields, table)}
'''

    def _generate_create_table_migration(self, entity: Dict[str, Any]) -> str:
        """Generate migration to create a table."""
        table_name = entity["name"].lower() + "s"
        fields = entity.get("fields", {})

        columns = ["        sa.Column('id', sa.Integer(), primary_key=True)"]

        for field_name, field_type in fields.items():
            columns.append(f"        sa.Column('{field_name}', sa.{field_type}())")

        columns.append("        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now())")
        columns.append("        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now())")

        columns_str = ",\n".join(columns)

        return f'''"""
Create {table_name} table

Revision ID: <generated>
"""

from alembic import op
import sqlalchemy as sa


revision = '<generated>'
down_revision = None


def upgrade() -> None:
    """Create {table_name} table."""
    op.create_table(
        '{table_name}',
{columns_str}
    )


def downgrade() -> None:
    """Drop {table_name} table."""
    op.drop_table('{table_name}')
'''

    def _generate_index_migration(
        self,
        table: str,
        indexes: List[Dict[str, Any]]
    ) -> str:
        """Generate migration for creating indexes."""
        operations = []

        for index in indexes:
            columns = index.get("columns", [])
            name = index.get("name")
            unique = index.get("unique", False)

            columns_str = ", ".join([f"'{col}'" for col in columns])

            operations.append(
                f"    op.create_index('{name}', '{table}', [{columns_str}], "
                f"unique={unique})"
            )

        upgrade_ops = "\n".join(operations)

        return f'''"""
Create indexes on {table}

Revision ID: <generated>
"""

from alembic import op


revision = '<generated>'
down_revision = None


def upgrade() -> None:
    """Create indexes."""
{upgrade_ops}


def downgrade() -> None:
    """Drop indexes."""
    # TODO: Add drop index operations
    pass
'''

    def _generate_foreign_key_migration(
        self,
        relationships: List[Dict[str, str]]
    ) -> str:
        """Generate migration for foreign key constraints."""
        operations = []

        for rel in relationships:
            from_table = rel["from_table"]
            from_column = rel["from_column"]
            to_table = rel["to_table"]
            to_column = rel["to_column"]

            fk_name = f"fk_{from_table}_{from_column}_{to_table}"

            operations.append(
                f"    op.create_foreign_key(\n"
                f"        '{fk_name}',\n"
                f"        '{from_table}', '{to_table}',\n"
                f"        ['{from_column}'], ['{to_column}']\n"
                f"    )"
            )

        upgrade_ops = "\n".join(operations)

        return f'''"""
Create foreign key constraints

Revision ID: <generated>
"""

from alembic import op


revision = '<generated>'
down_revision = None


def upgrade() -> None:
    """Create foreign keys."""
{upgrade_ops}


def downgrade() -> None:
    """Drop foreign keys."""
    # TODO: Add drop foreign key operations
    pass
'''

    def _generate_reverse_operations(
        self,
        fields: Dict[str, str],
        table: str
    ) -> str:
        """Generate reverse operations for rollback."""
        operations = []

        for field_name in fields.keys():
            operations.append(f"    op.drop_column('{table}', '{field_name}')")

        return "\n".join(operations)
