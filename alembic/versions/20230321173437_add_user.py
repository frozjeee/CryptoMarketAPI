"""add_user

Revision ID: fdfcaccc32e3
Revises: 2ae68dfd2304
Create Date: 2023-03-21 17:34:37.906481

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = 'fdfcaccc32e3'
down_revision = '2ae68dfd2304'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint("uix_country_id", 'country', ['id'])
    op.create_unique_constraint("uix_currency_id", 'currency', ['id'])
    op.create_unique_constraint("uix_currency_history_id", 'currency_history', ['id'])
    op.create_unique_constraint("uix_money_id", 'money', ['id'])
    op.create_unique_constraint("uix_order_id", 'order', ['id'])
    op.create_unique_constraint("uix_user_id", 'user', ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("uix_user_id", 'user', type_='unique')
    op.drop_constraint("uix_order_id", 'order', type_='unique')
    op.drop_constraint("uix_money_id", 'money', type_='unique')
    op.drop_constraint("uix_currency_history_id", 'currency_history', type_='unique')
    op.drop_constraint("uix_currency_id", 'currency', type_='unique')
    op.drop_constraint("uix_country_id", 'country', type_='unique')
    # ### end Alembic commands ###