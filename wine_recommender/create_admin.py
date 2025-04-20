import os
import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.append(str(Path(__file__).parent))

from app import create_app
from models.user.user import User
from models.common.base import db
from models.common.enums import UserRole

def create_admin_user():
    # Create Flask app with development config
    app = create_app('development')
    
    with app.app_context():
        # Initialize database if it doesn't exist
        db.create_all()
        
        # Check if admin already exists
        admin = User.query.filter_by(email='admin@wineapp.com').first()
        if not admin:
            # Create admin user
            admin = User.create_user(
                email='admin@wineapp.com',
                password='Admin123!',
                name='Admin User'
            )
            admin.is_admin = True
            admin.role = UserRole.ADMIN
            db.session.commit()
            print("Admin user created successfully!")
            print("Email: admin@wineapp.com")
            print("Password: Admin123!")
        else:
            print("Admin user already exists!")

if __name__ == '__main__':
    create_admin_user() 