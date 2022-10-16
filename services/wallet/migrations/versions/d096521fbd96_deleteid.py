"""deleteId

Revision ID: d096521fbd96
Revises: 845d8a805d0d
Create Date: 2022-07-07 10:25:01.876028

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'd096521fbd96'
down_revision = '845d8a805d0d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('wallet_id_key', 'wallet', type_='unique')
    op.drop_column('wallet', 'id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('wallet', sa.Column('id', postgresql.UUID(), autoincrement=False, nullable=False))
    op.create_unique_constraint('wallet_id_key', 'wallet', ['id'])
    # ### end Alembic commands ###
