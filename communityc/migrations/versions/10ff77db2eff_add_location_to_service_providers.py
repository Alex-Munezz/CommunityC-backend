"""add location to service providers

Revision ID: 10ff77db2eff
Revises: 1b370399c1c8
Create Date: 2024-10-07 13:53:47.672215

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '10ff77db2eff'
down_revision = '1b370399c1c8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('service_providers', schema=None) as batch_op:
        batch_op.add_column(sa.Column('location', sa.String(length=100), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('service_providers', schema=None) as batch_op:
        batch_op.drop_column('location')

    # ### end Alembic commands ###