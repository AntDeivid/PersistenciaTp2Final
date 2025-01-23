"""coluna apelido no usuario

Revision ID: 8efbd711667a
Revises: f73da4785ebd
Create Date: 2025-01-22 23:23:50.550302

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '8efbd711667a'
down_revision: Union[str, None] = 'f73da4785ebd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
