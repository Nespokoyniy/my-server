"""add another table

Revision ID: 54a155a92c94
Revises: 9a472321d342
Create Date: 2025-05-21 17:29:24.238906

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '54a155a92c94'
down_revision: Union[str, None] = '9a472321d342'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
