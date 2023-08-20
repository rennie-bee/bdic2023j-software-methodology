"""empty message

Revision ID: 72c842425e6c
Revises: 0b7bb3d89ab2
Create Date: 2021-11-30 01:02:56.006185

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '72c842425e6c'
down_revision = '0b7bb3d89ab2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('applications', schema=None) as batch_op:
        batch_op.add_column(sa.Column('filename', sa.String(length=64), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('applications', schema=None) as batch_op:
        batch_op.drop_column('filename')

    # ### end Alembic commands ###
