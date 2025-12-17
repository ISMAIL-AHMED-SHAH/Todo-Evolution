"""fix_user_table_constraints

Revision ID: 353d19d8f7af
Revises: 002_phase2_task_fields
Create Date: 2025-12-17 13:03:47.901388

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = '353d19d8f7af'
down_revision = '002_phase2_task_fields'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add server defaults for created_at and updated_at in user table
    # Using server_default to ensure database-level defaults
    op.alter_column('user', 'created_at',
                    existing_type=sa.DateTime(),
                    server_default=sa.text('CURRENT_TIMESTAMP'),
                    existing_nullable=False)

    op.alter_column('user', 'updated_at',
                    existing_type=sa.DateTime(),
                    server_default=sa.text('CURRENT_TIMESTAMP'),
                    existing_nullable=False)

    # Add index on user.email (model has index=True but migration was missing it)
    op.create_index('ix_user_email', 'user', ['email'])

    # Add server defaults for task table timestamps as well
    op.alter_column('task', 'created_at',
                    existing_type=sa.DateTime(),
                    server_default=sa.text('CURRENT_TIMESTAMP'),
                    existing_nullable=False)

    op.alter_column('task', 'updated_at',
                    existing_type=sa.DateTime(),
                    server_default=sa.text('CURRENT_TIMESTAMP'),
                    existing_nullable=False)


def downgrade() -> None:
    # Remove server defaults
    op.alter_column('task', 'updated_at',
                    existing_type=sa.DateTime(),
                    server_default=None,
                    existing_nullable=False)

    op.alter_column('task', 'created_at',
                    existing_type=sa.DateTime(),
                    server_default=None,
                    existing_nullable=False)

    # Remove index on user.email
    op.drop_index('ix_user_email', table_name='user')

    # Remove server defaults from user table
    op.alter_column('user', 'updated_at',
                    existing_type=sa.DateTime(),
                    server_default=None,
                    existing_nullable=False)

    op.alter_column('user', 'created_at',
                    existing_type=sa.DateTime(),
                    server_default=None,
                    existing_nullable=False)
