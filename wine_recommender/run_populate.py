import os
import sys

# Add the wine_recommender directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import and run the populate_wines script
from app import create_app
from scripts.populate_wines import populate_wines_from_data

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        wines_created = populate_wines_from_data()
        print(f"Total wines created: {wines_created}") 