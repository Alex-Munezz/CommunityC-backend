"""booking table

Revision ID: 0cff7033dbb0
Revises: 8ac062897733
Create Date: 2024-10-03 02:14:49.611612

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0cff7033dbb0'
down_revision = '8ac062897733'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('booking', schema=None) as batch_op:
        batch_op.add_column(sa.Column('service_name', sa.String(length=100), nullable=False))
        batch_op.drop_constraint('booking_service_id_fkey', type_='foreignkey')
        batch_op.drop_column('service_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('booking', schema=None) as batch_op:
        batch_op.add_column(sa.Column('service_id', sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.create_foreign_key('booking_service_id_fkey', 'service', ['service_id'], ['id'])
        batch_op.drop_column('service_name')

    # ### end Alembic commands ###
