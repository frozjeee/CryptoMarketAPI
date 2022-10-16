"""add_nullable

Revision ID: ea88a9bb7b71
Revises: ded0f13dc551
Create Date: 2022-05-26 19:30:56.312676

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'ea88a9bb7b71'
down_revision = 'ded0f13dc551'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('currency', 'code',
               existing_type=sa.VARCHAR(length=10),
               nullable=False)
    op.alter_column('currency', 'name',
               existing_type=sa.VARCHAR(length=50),
               nullable=False)
    op.alter_column('currency', 'price',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('currency', 'market_cap',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('currency_history', 'currency_id',
               existing_type=postgresql.UUID(),
               nullable=False)
    op.alter_column('currency_history', 'price',
               existing_type=postgresql.DOUBLE_PRECISION(precision=53),
               nullable=False)
    op.alter_column('currency_history', 'time',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('tick', 'currency_id',
               existing_type=postgresql.UUID(),
               nullable=False)
    op.alter_column('tick', 'tick_price',
               existing_type=postgresql.DOUBLE_PRECISION(precision=53),
               nullable=False)
    op.alter_column('tick', 'time',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('tick', 'time',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('tick', 'tick_price',
               existing_type=postgresql.DOUBLE_PRECISION(precision=53),
               nullable=True)
    op.alter_column('tick', 'currency_id',
               existing_type=postgresql.UUID(),
               nullable=True)
    op.alter_column('currency_history', 'time',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('currency_history', 'price',
               existing_type=postgresql.DOUBLE_PRECISION(precision=53),
               nullable=True)
    op.alter_column('currency_history', 'currency_id',
               existing_type=postgresql.UUID(),
               nullable=True)
    op.alter_column('currency', 'market_cap',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('currency', 'price',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('currency', 'name',
               existing_type=sa.VARCHAR(length=50),
               nullable=True)
    op.alter_column('currency', 'code',
               existing_type=sa.VARCHAR(length=10),
               nullable=True)
    # ### end Alembic commands ###
