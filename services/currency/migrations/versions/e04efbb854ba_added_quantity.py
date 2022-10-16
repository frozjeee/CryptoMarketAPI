"""added_quantity

Revision ID: e04efbb854ba
Revises: ea88a9bb7b71
Create Date: 2022-07-17 19:29:56.451137

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e04efbb854ba'
down_revision = 'ea88a9bb7b71'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('currency', sa.Column('quantity', sa.Float(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('currency', 'quantity')
    # ### end Alembic commands ###