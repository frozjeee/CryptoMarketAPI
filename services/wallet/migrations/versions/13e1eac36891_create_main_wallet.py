"""create_main_wallet

Revision ID: 13e1eac36891
Revises: d4da495ea2df
Create Date: 2022-09-06 13:43:33.985867

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '13e1eac36891'
down_revision = 'd4da495ea2df'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('main_wallet',
    sa.Column('id', postgresql.UUID(), nullable=False),
    sa.Column('user_id', postgresql.UUID(), nullable=True),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('code', sa.String(length=10), nullable=False),
    sa.Column('quantity', sa.Float(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('main_wallet')
    # ### end Alembic commands ###