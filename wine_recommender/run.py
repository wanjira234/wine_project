import os
from app import create_app

# Set the environment
os.environ['FLASK_ENV'] = 'development'
os.environ['FLASK_APP'] = 'run.py'

# Create the application instance
app = create_app()

if __name__ == '__main__':
    # Run the application
    app.run(debug=True, port=5000) 