"""create posts table

Revision ID: 181012850ada
Revises: 
Create Date: 2022-06-22 11:07:27.102880

"""
from alembic import op
import sqlalchemy as sa

# https://alembic.sqlalchemy.org/en/latest/api/ddl.html

# revision identifiers, used by Alembic.
revision = '181012850ada'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True), 
        sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
