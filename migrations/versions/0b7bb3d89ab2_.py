"""empty message

Revision ID: 0b7bb3d89ab2
Revises: 
Create Date: 2021-11-30 00:27:37.402975

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0b7bb3d89ab2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('applications',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('body', sa.Text(), nullable=False),
    sa.Column('student_id', sa.Integer(), nullable=True),
    sa.Column('recruitment_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['recruitment_id'], ['recruitments.id'], name=op.f('fk_applications_recruitment_id_recruitments')),
    sa.ForeignKeyConstraint(['student_id'], ['users.id'], name=op.f('fk_applications_student_id_users')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_applications'))
    )
    with op.batch_alter_table('applications', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_applications_timestamp'), ['timestamp'], unique=False)

    with op.batch_alter_table('roles', schema=None) as batch_op:
        batch_op.create_unique_constraint(batch_op.f('uq_roles_name'), ['name'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('roles', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('uq_roles_name'), type_='unique')

    with op.batch_alter_table('applications', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_applications_timestamp'))

    op.drop_table('applications')
    # ### end Alembic commands ###