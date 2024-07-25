"""create post table

Revision ID: 517a547b4954
Revises: 
Create Date: 2024-03-12 22:16:38.411181

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '517a547b4954'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'post',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('title', sa.String, nullable=False)
    )
    pass


def downgrade() -> None:
    op.drop_table("post")
    pass
