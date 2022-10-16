"""Init3

Revision ID: 525c813532d7
Revises: 09041d53dfe4
Create Date: 2022-05-05 19:23:03.874235

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '525c813532d7'
down_revision = '09041d53dfe4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('User', 'is_superuser',
               existing_type=sa.BOOLEAN(),
               nullable=False)
    op.alter_column('User', 'email',
               existing_type=sa.VARCHAR(length=250),
               nullable=False)
    op.alter_column('User', 'name',
               existing_type=sa.VARCHAR(length=250),
               nullable=False)
    op.alter_column('User', 'password',
               existing_type=sa.VARCHAR(length=250),
               nullable=False)
    op.alter_column('User', 'birthdate',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('User', 'country_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('User', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('User', 'updated_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('User', 'updated_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('User', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('User', 'country_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('User', 'birthdate',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('User', 'password',
               existing_type=sa.VARCHAR(length=250),
               nullable=True)
    op.alter_column('User', 'name',
               existing_type=sa.VARCHAR(length=250),
               nullable=True)
    op.alter_column('User', 'email',
               existing_type=sa.VARCHAR(length=250),
               nullable=True)
    op.alter_column('User', 'is_superuser',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    # ### end Alembic commands ###