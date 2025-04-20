import pandas as pd
import os
import sys

# Add the wine_recommender directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Read the data file
df = pd.read_pickle('../data/df_wine_clean.pkl')

# Print information about the DataFrame
print("DataFrame Info:")
print(df.info())

print("\nSample of first few rows:")
print(df.head())

def check_columns():
    try:
        # Read the clean wine data
        df_wine = pd.read_pickle('data/df_wine_clean.pkl')
        
        # Print just the column names
        print("Columns in the data:")
        for col in df_wine.columns:
            print(f"- {col}")
        
    except Exception as e:
        print(f"Error reading data: {str(e)}")

if __name__ == '__main__':
    check_columns() 