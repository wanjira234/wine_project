from app import app
from extensions import db

def init_db():
    """Initialize the database by creating all tables."""
    with app.app_context():
        # Create all tables
        db.create_all()
        print("Database tables created successfully!")

if __name__ == '__main__':
    init_db() 