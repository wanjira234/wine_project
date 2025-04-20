"""fix_database_structure

Revision ID: fix_database_structure
Revises: 41881940cb66
Create Date: 2024-03-31

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import sqlite


# revision identifiers, used by Alembic.
revision = 'fix_database_structure'
down_revision = '41881940cb66'
branch_labels = None
depends_on = None


def upgrade():
    # Drop the duplicate 'user' table
    op.drop_table('user')
    
    # Drop existing user_preferences table
    op.drop_table('user_preferences')
    
    # Create new user_preferences table with correct structure
    op.create_table('user_preferences',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('wine_experience', sqlite.JSON(), nullable=True),
        sa.Column('wine_style', sqlite.JSON(), nullable=True),
        sa.Column('wine_traits', sqlite.JSON(), nullable=True),
        sa.Column('wine_regions', sqlite.JSON(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Set default values for JSON columns
    op.execute("""
        UPDATE user_preferences 
        SET wine_experience = json('{"experience_level": "BEGINNER", "drinking_frequency": "OCCASIONALLY", "wine_types": []}'),
            wine_style = json('{"body_preference": "MEDIUM", "sweetness_level": "DRY", "price_ranges": {"regular": {"min": 15, "max": 50, "currency": "USD"}, "special": {"min": 50, "max": 200, "currency": "USD"}}}'),
            wine_traits = json('{"preferred_traits": []}'),
            wine_regions = json('{"preferred_regions": []}')
        WHERE wine_experience IS NULL
    """)


def downgrade():
    # Drop the new user_preferences table
    op.drop_table('user_preferences')
    
    # Recreate the original user_preferences table
    op.create_table('user_preferences',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('preferences_json', sa.Text(), nullable=True),
        sa.Column('wine_knowledge', sqlite.JSON(), nullable=True),
        sa.Column('wine_preferences', sqlite.JSON(), nullable=True),
        sa.Column('budget_preferences', sqlite.JSON(), nullable=True),
        sa.Column('taste_profile', sqlite.JSON(), nullable=True),
        sa.Column('rating_preferences', sqlite.JSON(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Recreate the user table
    op.create_table('user',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(length=80), nullable=False),
        sa.Column('email', sa.String(length=120), nullable=False),
        sa.Column('password_hash', sa.String(length=128), nullable=True),
        sa.Column('name', sa.String(length=128), nullable=True),
        sa.Column('role', sa.String(length=9), nullable=True),
        sa.Column('bio', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('preferences_json', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('username')
    ) 