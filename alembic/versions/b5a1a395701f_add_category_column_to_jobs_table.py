"""Add category column to jobs table

Revision ID: b5a1a395701f
Revises: 
Create Date: 2024-09-25 22:08:25.294334

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b5a1a395701f'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('jobs', sa.Column('category', sa.String(100), nullable=True))

def downgrade() -> None:
    op.drop_column('jobs', 'category')
