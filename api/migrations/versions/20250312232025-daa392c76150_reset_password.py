"""reset password

Revision ID: daa392c76150
Revises: a50e53b7ee31
Create Date: 2025-03-12 23:20:25.083897

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'daa392c76150'
down_revision: Union[str, None] = 'a50e53b7ee31'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('reset_password_token', sa.String(), nullable=True))
    op.add_column('user', sa.Column('reset_password_expires', sa.DateTime(timezone=True), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'reset_password_expires')
    op.drop_column('user', 'reset_password_token')
    # ### end Alembic commands ###
