import os
import sys

# Add the parent directory to Python path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from flask import Flask
from extensions import db
from models.settings.settings import Settings

def create_settings_table():
    """Create the settings table in the database."""
    # Create a new Flask app
    app = Flask(__name__)
    
    # Ensure instance directory exists
    instance_path = os.path.join(parent_dir, 'instance')
    os.makedirs(instance_path, exist_ok=True)
    
    # Configure the app
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(instance_path, "wine_recommender.db")}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize the database
    db.init_app(app)
    
    with app.app_context():
        try:
            # Create the table
            db.create_all()
            
            # Add default settings
            default_settings = [
                ('site_name', 'Wine Recommender', 'Name of the website'),
                ('site_description', 'Your personal wine recommendation system', 'Description of the website'),
                ('low_stock_threshold', '10', 'Threshold for low stock warning'),
                ('default_stock', '50', 'Default stock level for new wines'),
                ('smtp_server', '', 'SMTP server for email notifications'),
                ('smtp_port', '587', 'SMTP port for email notifications'),
                ('smtp_username', '', 'SMTP username for email notifications'),
                ('smtp_password', '', 'SMTP password for email notifications')
            ]
            
            for key, value, description in default_settings:
                # Check if setting already exists
                setting = Settings.query.filter_by(key=key).first()
                if not setting:
                    setting = Settings(key=key, value=value, description=description)
                    db.session.add(setting)
            
            db.session.commit()
            print("Settings table created and default settings added successfully.")
        except Exception as e:
            print(f"Error: {str(e)}")
            db.session.rollback()
        finally:
            db.session.close()

if __name__ == '__main__':
    create_settings_table() 