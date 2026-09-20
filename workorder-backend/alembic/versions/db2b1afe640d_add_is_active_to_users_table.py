"""Add is_active to users table

Revision ID: db2b1afe640d
Revises: 6bc76e4898d9
Create Date: 2026-09-19 22:38:20.891184

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'db2b1afe640d'
down_revision: Union[str, Sequence[str], None] = '6bc76e4898d9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('users', sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('true')))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('users', 'is_active')