import os
from flask import Flask
from config import config
from extensions import init_extensions, db, login_manager, csrf
from models.user.user import User
from routes.auth import auth
from routes.main import main
from routes.admin import admin
from commands import init_app as init_commands

def create_app(config_name=None):
    """Create and configure the Flask application."""
    if config_name is None:
        # Default to development if not explicitly set to production
        config_name = os.environ.get('FLASK_ENV', 'development')
        if config_name not in config:
            config_name = 'development'
    
    app = Flask(__name__)
    
    # Use development config by default
    if config_name == 'production' and not os.environ.get('SECRET_KEY'):
        config_name = 'development'
        print("Warning: Production environment detected but no SECRET_KEY set. Falling back to development configuration.")
    
    app.config.from_object(config[config_name])
    
    # Initialize wine traits
    from models.common.enums import WineTrait
    app.all_traits = [trait.value for trait in WineTrait]
    
    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # Ensure the upload folder exists
    try:
        os.makedirs(app.config['UPLOAD_FOLDER'])
    except OSError:
        pass
    
    # Initialize extensions
    init_extensions(app)
    
    # Register blueprints
    app.register_blueprint(auth)
    app.register_blueprint(main)
    app.register_blueprint(admin, url_prefix='/admin')
    
    # Initialize commands
    init_commands(app)
    
    return app

app = create_app()
