"""added_tick

Revision ID: 68b913794188
Revises: b15dcee0d38f
Create Date: 2022-05-15 17:17:32.582052

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '68b913794188'
down_revision = 'b15dcee0d38f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tick',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('currency_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('tick_price', sa.Float(), nullable=False),
    sa.Column('time', sa.TIMESTAMP(), nullable=False),
    sa.ForeignKeyConstraint(['currency_id'], ['currency.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.add_column('currency_history', sa.Column('price', sa.Float(), nullable=False))
    op.drop_column('currency_history', 'tick_price')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('currency_history', sa.Column('tick_price', postgresql.UUID(), autoincrement=False, nullable=False))
    op.drop_column('currency_history', 'price')
    op.drop_table('tick')
    # ### end Alembic commands ###
