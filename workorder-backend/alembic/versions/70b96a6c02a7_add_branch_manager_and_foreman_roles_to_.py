"""Add Branch Manager and Foreman roles to UserRole enum

Revision ID: 70b96a6c02a7
Revises: db2b1afe640d
Create Date: 2026-09-20 16:59:21.185270

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '70b96a6c02a7'
down_revision: Union[str, Sequence[str], None] = 'db2b1afe640d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add new enum values to userrole enum
    op.execute("ALTER TYPE userrole ADD VALUE IF NOT EXISTS 'branch_manager'")
    op.execute("ALTER TYPE userrole ADD VALUE IF NOT EXISTS 'foreman'")


def downgrade() -> None:
    """Downgrade schema."""
    # Note: Removing enum values is not straightforward in PostgreSQL
    # To properly downgrade, you would need to recreate the type without the values
    # This is left as a manual operation if needed
    pass
