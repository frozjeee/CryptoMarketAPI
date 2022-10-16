"""fixAmount

Revision ID: 4189bbf0f5b4
Revises: c52c0517978f
Create Date: 2022-08-31 17:11:57.085772

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4189bbf0f5b4'
down_revision = 'c52c0517978f'
branch_labels = None
depends_on = None


def upgrade():
    op.execute('ALTER TABLE wallet ALTER COLUMN amount TYPE double precision USING amount::double precision')


def downgrade():
    pass
