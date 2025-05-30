"""assessment response creator

Revision ID: a50e53b7ee31
Revises: 622c6317872f
Create Date: 2025-03-10 19:54:26.693093

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'a50e53b7ee31'
down_revision: Union[str, None] = '622c6317872f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('assessmentresponse', sa.Column('created_by', sa.Uuid(), nullable=False))
    op.create_foreign_key(None, 'assessmentresponse', 'account', ['created_by'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'assessmentresponse', type_='foreignkey')
    op.drop_column('assessmentresponse', 'created_by')
    # ### end Alembic commands ###
