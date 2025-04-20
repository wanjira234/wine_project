import pandas as pd
import numpy as np
from models.wine.wine import Wine
from models.common.enums import WineType, WineRegion
from extensions import db
import os
import traceback

def determine_wine_type(variety, description):
    """Determine wine type from variety and description."""
    variety_desc = f"{variety} {description}".lower()
    if 'red' in variety_desc or 'cabernet' in variety_desc or 'merlot' in variety_desc or 'pinot noir' in variety_desc:
        return WineType.RED
    elif 'white' in variety_desc or 'chardonnay' in variety_desc or 'sauvignon' in variety_desc or 'riesling' in variety_desc:
        return WineType.WHITE
    elif 'rose' in variety_desc or 'rosé' in variety_desc or 'rosato' in variety_desc:
        return WineType.ROSE
    elif 'sparkling' in variety_desc or 'champagne' in variety_desc or 'prosecco' in variety_desc:
        return WineType.SPARKLING
    elif 'dessert' in variety_desc or 'port' in variety_desc or 'sauternes' in variety_desc:
        return WineType.DESSERT
    return WineType.RED  # Default to red if can't determine

def map_wine_region(region_1, region_2, province):
    """Map region to WineRegion enum."""
    region_str = f"{region_1} {region_2} {province}".lower()
    
    region_map = {
        'bordeaux': WineRegion.BORDEAUX,
        'burgundy': WineRegion.BURGUNDY,
        'champagne': WineRegion.CHAMPAGNE,
        'rhone': WineRegion.RHONE,
        'loire': WineRegion.LOIRE,
        'provence': WineRegion.PROVENCE,
        'tuscany': WineRegion.TUSCANY,
        'piedmont': WineRegion.PIEDMONT,
        'veneto': WineRegion.VENETO,
        'sicily': WineRegion.SICILY,
        'rioja': WineRegion.RIOJA,
        'ribera del duero': WineRegion.RIBERA_DEL_DUERO,
        'priorat': WineRegion.PRIORAT,
        'napa valley': WineRegion.NAPA_VALLEY,
        'sonoma': WineRegion.SONOMA,
        'oregon': WineRegion.OREGON,
        'washington': WineRegion.WASHINGTON,
        'mosel': WineRegion.MOSEL,
        'douro': WineRegion.DOURO,
        'barossa': WineRegion.BAROSSA,
        'marlborough': WineRegion.MARLBOROUGH,
        'mendoza': WineRegion.MENDOZA,
        'stellenbosch': WineRegion.STELLENBOSCH,
        'casablanca': WineRegion.CASABLANCA
    }
    
    # Try to find the best matching region
    for key, value in region_map.items():
        if key in region_str:
            return value
    return WineRegion.NAPA_VALLEY  # Default to Napa Valley if no match

def populate_wines_from_data():
    """Populate database with wines from the data files."""
    try:
        print("Starting to populate wines...")
        # Get the absolute path to the data file
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_dir = os.path.dirname(script_dir)  # wine_recommender directory
        data_file = os.path.join(project_dir, 'data', 'df_wine_clean.pkl')
        
        # Read the clean wine data
        print(f"Attempting to read data file from: {data_file}")
        df_wine = pd.read_pickle(data_file)
        print(f"Successfully read data file with {len(df_wine)} rows")
        
        # Create wines from the data
        wines_created = 0
        for _, row in df_wine.iterrows():
            try:
                # Handle missing or NaN values
                name = str(row['title']) if pd.notna(row['title']) else "Unknown Wine"
                variety = str(row['variety']) if pd.notna(row['variety']) else ""
                description = str(row['description']) if pd.notna(row['description']) else ""
                region = map_wine_region(
                    str(row['region_1']) if pd.notna(row['region_1']) else "",
                    str(row['region_2']) if pd.notna(row['region_2']) else "",
                    str(row['province']) if pd.notna(row['province']) else ""
                )
                price = float(row['price']) if pd.notna(row['price']) else 0.0
                
                # Determine wine type from variety and description
                wine_type = determine_wine_type(variety, description)
                
                wine = Wine.create_wine(
                    name=name,
                    type=wine_type,
                    region=region,
                    price=price,
                    year=None,  # No year in the data
                    description=description,
                    stock=50,  # Default stock level
                    image_url=None  # No image URLs in the data
                )
                wines_created += 1
                
                if wines_created % 100 == 0:
                    print(f"Created {wines_created} wines so far...")
                    
            except Exception as e:
                print(f"Error creating wine {row.get('title', 'Unknown')}: {str(e)}")
                print(f"Full error: {traceback.format_exc()}")
                continue
        
        print(f"Successfully created {wines_created} wines in the database")
        return wines_created
        
    except Exception as e:
        print(f"Error reading wine data: {str(e)}")
        print(f"Full error: {traceback.format_exc()}")
        return 0

if __name__ == '__main__':
    # Populate wines from data
    wines_created = populate_wines_from_data()
    print(f"Total wines created: {wines_created}") 