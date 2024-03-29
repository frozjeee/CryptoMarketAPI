"""Init

Revision ID: 4a6d7db789ce
Revises: 
Create Date: 2022-06-16 17:50:01.775205

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import db
# revision identifiers, used by Alembic.
revision = '4a6d7db789ce'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('order',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('currency_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('type', db.OrderType(), nullable=False),
    sa.Column('amount', sa.Float(), nullable=False),
    sa.Column('status', db.OrderStatus(), nullable=False),
    sa.Column('ordered_at', sa.TIMESTAMP(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('type')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('order')
    # ### end Alembic commands ###
