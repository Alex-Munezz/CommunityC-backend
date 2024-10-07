"""add password to service providers

Revision ID: 1b370399c1c8
Revises: 660f72e12c7d
Create Date: 2024-10-07 13:46:23.562099

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1b370399c1c8'
down_revision = '660f72e12c7d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('service_providers', schema=None) as batch_op:
        batch_op.add_column(sa.Column('password', sa.String(length=128), nullable=False))
        batch_op.drop_column('location')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('service_providers', schema=None) as batch_op:
        batch_op.add_column(sa.Column('location', sa.VARCHAR(length=100), autoincrement=False, nullable=False))
        batch_op.drop_column('password')

    # ### end Alembic commands ###
