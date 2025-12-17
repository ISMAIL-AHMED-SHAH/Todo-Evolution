"""Add Phase 2 task fields (priority, category, due_date)

Revision ID: 002_phase2_task_fields
Revises: 2025_12_09_0858
Create Date: 2025-12-13

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSON

# revision identifiers, used by Alembic.
revision = '002_phase2_task_fields'
down_revision = '2025_12_09_0858'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add Phase 2 enhancements to task table."""
    # Add priority column with default 'Medium'
    op.add_column('task',
        sa.Column('priority', sa.String(10),
                  nullable=False,
                  server_default='Medium'))

    # Add category column (JSON array)
    op.add_column('task',
        sa.Column('category', JSON,
                  nullable=False,
                  server_default='[]'))

    # Add due_date column (nullable)
    op.add_column('task',
        sa.Column('due_date', sa.Date, nullable=True))

    # Create index on due_date for efficient overdue queries
    op.create_index('ix_task_due_date', 'task', ['due_date'])


def downgrade() -> None:
    """Remove Phase 2 enhancements from task table."""
    op.drop_index('ix_task_due_date', table_name='task')
    op.drop_column('task', 'due_date')
    op.drop_column('task', 'category')
    op.drop_column('task', 'priority')
