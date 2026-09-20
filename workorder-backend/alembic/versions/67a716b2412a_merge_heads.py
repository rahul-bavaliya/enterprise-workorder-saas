"""Merge heads

Revision ID: 67a716b2412a
Revises: aabc391e7271, c45674ce64a8
Create Date: 2026-09-18 22:31:18.978719

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '67a716b2412a'
down_revision: Union[str, Sequence[str], None] = ('aabc391e7271', 'c45674ce64a8')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
