"""add refresh_token

Revision ID: adab90be4d9a
Revises: cc4da6ab784f
Create Date: 2021-03-13 12:52:25.703592

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql


# revision identifiers, used by Alembic.
revision = 'adab90be4d9a'
down_revision = 'cc4da6ab784f'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('user', sa.Column('refresh_token', mysql.VARCHAR(length=500), nullable=True))


def downgrade():
    pass
