"""Create tasks table

Revision ID: 002_create_tasks
Revises: 001_create_users
Create Date: 2025-12-14 10:05:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = '002_create_tasks'
down_revision = '001_create_users'
branch_labels = None
depends_on = None


def upgrade():
    # Create tasks table
    op.create_table(
        'tasks',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('gen_random_uuid()'), nullable=False),
        sa.Column('title', sa.String(200), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('is_completed', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # Create indexes
    op.create_index('ix_tasks_user_id', 'tasks', ['user_id'])
    op.create_index('ix_tasks_user_created', 'tasks', ['user_id', 'created_at'], postgresql_ops={'created_at': 'DESC'})


def downgrade():
    op.drop_index('ix_tasks_user_created', table_name='tasks')
    op.drop_index('ix_tasks_user_id', table_name='tasks')
    op.drop_table('tasks')