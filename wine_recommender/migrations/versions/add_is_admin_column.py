"""Add is_admin column to users table

Revision ID: add_is_admin_column
Revises: fix_database_structure
Create Date: 2024-04-01

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_is_admin_column'
down_revision = 'fix_database_structure'
branch_labels = None
depends_on = None


def upgrade():
    # Add is_admin column with default value False
    op.add_column('users', sa.Column('is_admin', sa.Boolean(), nullable=False, server_default='0'))
    
    # Update the first user (id=1) to be an admin
    op.execute("UPDATE users SET is_admin = 1 WHERE id = 1")


def downgrade():
    # Remove is_admin column
    op.drop_column('users', 'is_admin') 