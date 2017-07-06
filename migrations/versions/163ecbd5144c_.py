"""empty message

Revision ID: 163ecbd5144c
Revises: 
Create Date: 2017-07-03 10:40:17.936582

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '163ecbd5144c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Rate')
    op.drop_table('Users')
    op.drop_table('JobsDetails')
    op.drop_table('Jobs')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Jobs',
    sa.Column('job_id', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('job_name', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('date_created', sa.DATE(), autoincrement=False, nullable=True),
    sa.Column('date_completed', sa.DATE(), autoincrement=False, nullable=True),
    sa.Column('competed', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.Column('verbatim', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.Column('timestamp', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.Column('paid', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.Column('duration', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('download_link', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('description', sa.TEXT(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('job_id', name='Jobs_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('JobsDetails',
    sa.Column('job_details_id', sa.INTEGER(), server_default=sa.text('nextval(\'"JobsDetails_job_details_id_seq"\'::regclass)'), nullable=False),
    sa.Column('job_name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('paid', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.Column('date_created', sa.DATE(), autoincrement=False, nullable=True),
    sa.Column('date_completed', sa.DATE(), autoincrement=False, nullable=True),
    sa.Column('competed', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.Column('duration', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('download_link', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('description', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('user', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('job', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['job'], ['Jobs.job_id'], name='JobsDetails_job_fkey'),
    sa.ForeignKeyConstraint(['user'], ['Users.user_id'], name='JobsDetails_user_fkey'),
    sa.PrimaryKeyConstraint('job_details_id', name='JobsDetails_pkey')
    )
    op.create_table('Users',
    sa.Column('user_id', sa.INTEGER(), server_default=sa.text('nextval(\'"Users_user_id_seq"\'::regclass)'), nullable=False),
    sa.Column('first_name', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('last_name', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('email', sa.VARCHAR(length=200), autoincrement=False, nullable=False),
    sa.Column('hash_password', sa.VARCHAR(length=1000), autoincrement=False, nullable=True),
    sa.Column('date_added', sa.DATE(), autoincrement=False, nullable=True),
    sa.Column('date_modified', sa.DATE(), autoincrement=False, nullable=True),
    sa.Column('role', sa.VARCHAR(length=20), autoincrement=False, nullable=False),
    sa.Column('availability', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.Column('account_access', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.Column('availability_date_update', sa.DATE(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('user_id', name='Users_pkey'),
    sa.UniqueConstraint('email', name='Users_email_key')
    )
    op.create_table('Rate',
    sa.Column('rate_id', sa.INTEGER(), server_default=sa.text('nextval(\'"Rate_rate_id_seq"\'::regclass)'), nullable=False),
    sa.Column('rate', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('description', sa.TEXT(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('rate_id', name='Rate_pkey')
    )
    # ### end Alembic commands ###