"""add creator

Revision ID: ce53b8cadb45
Revises: df645a2b33c0
Create Date: 2023-06-07 18:31:00.878690

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ce53b8cadb45'
down_revision = 'df645a2b33c0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('order', sa.Column('created_by', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'order', 'user', ['created_by'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'order', type_='foreignkey')
    op.drop_column('order', 'created_by')
    # ### end Alembic commands ###
