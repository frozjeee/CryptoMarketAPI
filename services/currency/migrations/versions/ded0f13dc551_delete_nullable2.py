"""delete_nullable2

Revision ID: ded0f13dc551
Revises: 8402da057de7
Create Date: 2022-05-26 19:29:07.079257

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ded0f13dc551'
down_revision = '8402da057de7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('currency', 'code',
               existing_type=sa.VARCHAR(length=10),
               nullable=True)
    op.alter_column('currency', 'name',
               existing_type=sa.VARCHAR(length=50),
               nullable=True)
    op.alter_column('currency', 'price',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('currency', 'market_cap',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('currency', 'market_cap',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('currency', 'price',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('currency', 'name',
               existing_type=sa.VARCHAR(length=50),
               nullable=False)
    op.alter_column('currency', 'code',
               existing_type=sa.VARCHAR(length=10),
               nullable=False)
    # ### end Alembic commands ###
