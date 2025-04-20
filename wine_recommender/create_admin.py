"""
Script to create an admin user in the database.
"""

import os
import sys
from getpass import getpass
from app import create_app
from extensions import db
from models.user.user import User

def create_admin_user(email, password, name=None):
    """Create a new admin user."""
    try:
        # Create user
        user = User.create_user(email=email, password=password, name=name)
        user.is_admin = True
        db.session.commit()
        print(f"Admin user '{email}' created successfully!")
        return True
    except Exception as e:
        print(f"Error creating admin user: {e}")
        return False

def main():
    """Main function to create admin user."""
    app = create_app('development')
    
    with app.app_context():
        # Get admin user details
        email = input("Enter admin email: ")
        password = getpass("Enter admin password: ")
        confirm_password = getpass("Confirm password: ")
        
        if password != confirm_password:
            print("Passwords do not match!")
            sys.exit(1)
        
        name = input("Enter admin name (optional): ").strip() or None
        
        # Create admin user
        if create_admin_user(email, password, name):
            sys.exit(0)
        else:
            sys.exit(1)

if __name__ == '__main__':
    main() 