"""add_init_quantity

Revision ID: df645a2b33c0
Revises: e0f7809a1503
Create Date: 2023-05-13 18:56:52.066235

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'df645a2b33c0'
down_revision = 'e0f7809a1503'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('order', sa.Column('init_quantity', sa.DECIMAL(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('order', 'init_quantity')
    # ### end Alembic commands ###