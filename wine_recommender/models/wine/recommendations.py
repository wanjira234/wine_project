from ..common.enums import WineType, BodyType, SweetnessLevel
from flask import current_app
import pandas as pd
import numpy as np
import os
from models.user.preferences import UserPreference
from models.user.user import User
from pprint import pprint

class WineRecommender(User):
    """Wine recommendation engine."""
    
    def __init__(self, user=None):
        """Initialize recommender with wine data from pickle files."""
        self.user_id = user.id
        self.df_clean = pd.read_pickle('data/df_wine_clean.pkl')
        self.df_combi = pd.read_pickle('data/df_wine_combi.pkl')
        self.df_us_rate = pd.read_pickle('data/df_wine_us_rate.pkl')
        
        # Merge dataframes to get the most comprehensive dataset
        self.df = self.df_combi.copy()
        # Add any missing columns from df_clean
        missing_cols = set(self.df_clean.columns) - set(self.df.columns)
        for col in missing_cols:
            self.df[col] = self.df_clean[col]
        
        # Add US ratings if available
        if not self.df_us_rate.empty:
            self.df = self.df.merge(self.df_us_rate[['title', 'points']], 
                                  on='title', how='left', suffixes=('', '_us'))
        
        # Fill missing values
        self.df['price'] = self.df['price'].fillna(self.df['price'].mean())
        self.df['points'] = self.df['points'].fillna(self.df['points'].mean())
        
        # Use the DataFrame index as the persistent ID
        self.df['id'] = self.df.index.astype(str)
        self.user_preferences = user.get_preferences()

    def get_recommendations(self, filters=None, limit=20):
        """Get wine recommendations based on filters."""
        try:
            # Start with all wines
            filtered_df = self.df.copy()

            # === Apply preferences ===
            if self.user_preferences:
                pprint({k: v for k, v in self.user_preferences.items()})
                wine_types = self.user_preferences.get('wine_types', [])
                wine_traits = self.user_preferences.get('wine_traits', [])
                wine_regions = self.user_preferences.get('wine_regions', [])
                wine_style = self.user_preferences.get('wine_style', {})

                price_ranges = wine_style.get('price_ranges', {})
                min_price = price_ranges.get('regular', {}).get('min')
                max_price = price_ranges.get('special', {}).get('max')

                # filter by price ranges
                if min_price and max_price:
                    filtered_df = filtered_df[(filtered_df['price'] >= min_price) & (filtered_df['price'] <= max_price)]
                
                # filter by wine_types
                if wine_types:
                    #filtered_df = filtered_df[filtered_df['variety'].str.lower().isin([t.lower() for t in wine_types])]
                    for wt in wine_types:
                        if wt in filtered_df.columns:
                            filtered_df = filtered_df[filtered_df[wt] == 1]
                
                # filter by wine traits
                if wine_traits:
                    # filter traits that actually exist in the DataFrame
                    valid_traits = [trait for trait in wine_traits if trait in filtered_df.columns]
                    if valid_traits:
                        # create a combined boolean mask using OR logic across columns
                        trait_mask = filtered_df[valid_traits].any(axis=1)
                        filtered_df = filtered_df[trait_mask]
                
                '''
                # filter by regions <DISABLED>
                filtered_df['region_1'] = filtered_df['region_1'].astype(str).str.strip().str.lower()
                filtered_df['region_2'] = filtered_df['region_2'].astype(str).str.strip().str.lower()
                
                if wine_regions:
                    wine_regions_normalized = [r.replace('_', ' ').lower().strip() for r in wine_regions]

                    region_mask = (
                        filtered_df['region_1'].isin(wine_regions_normalized) |
                        filtered_df['region_2'].isin(wine_regions_normalized)
                    )
                    print(region_mask)
                    filtered_df = filtered_df[region_mask]
                    print(filtered_df)'''
            
            # Apply filters if provided
            if filters:
                if filters.get('country'):
                    filtered_df = filtered_df[filtered_df['country'].str.lower() == filters['country'].lower()]
                
                if filters.get('province'):
                    filtered_df = filtered_df[filtered_df['province'].str.lower() == filters['province'].lower()]
                
                if filters.get('variety'):
                    filtered_df = filtered_df[filtered_df['variety'].str.lower() == filters['variety'].lower()]
                
                if filters.get('taster'):
                    filtered_df = filtered_df[filtered_df['taster_name'].str.lower() == filters['taster'].lower()]
                
                if filters.get('min_points'):
                    filtered_df = filtered_df[filtered_df['points'] >= filters['min_points']]
                
                if filters.get('max_price'):
                    filtered_df = filtered_df[filtered_df['price'] <= filters['max_price']]
            
            # Sort by points and limit results
            filtered_df = filtered_df.sort_values('points', ascending=False).head(limit)
            
            # Convert to list of dictionaries
            recommendations = filtered_df.to_dict('records')
            
            # Ensure IDs are strings for consistency
            for rec in recommendations:
                rec['id'] = str(rec['id'])
            
            return recommendations
            
        except Exception as e:
            if hasattr(current_app, 'logger'):
                current_app.logger.error(f"Error getting recommendations: {str(e)}")
            return []

    def _apply_filters(self, df, filters):
        """Apply filters to the wine dataframe."""
        filtered_df = df.copy()
        
        # Apply country filter
        if filters.get('country'):
            filtered_df = filtered_df[filtered_df['country'].str.lower() == filters['country'].lower()]
        
        # Apply province filter
        if filters.get('province'):
            filtered_df = filtered_df[filtered_df['province'].str.lower() == filters['province'].lower()]
        
        # Apply winery filter
        if filters.get('winery'):
            filtered_df = filtered_df[filtered_df['winery'].str.lower() == filters['winery'].lower()]
        
        # Apply variety filter
        if filters.get('variety'):
            filtered_df = filtered_df[filtered_df['variety'].str.lower() == filters['variety'].lower()]
        
        # Apply designation filter
        if filters.get('designation'):
            filtered_df = filtered_df[filtered_df['designation'].str.lower() == filters['designation'].lower()]
        
        # Apply minimum rating filter
        if filters.get('min_rating'):
            filtered_df = filtered_df[filtered_df['points'] >= float(filters['min_rating'])]
        
        return filtered_df

    def _apply_basic_filters(self, df, filters):
        """Apply only basic filters to broaden the search."""
        filtered_df = df.copy()
        
        # Only apply country and minimum rating filters
        if filters.get('country'):
            filtered_df = filtered_df[filtered_df['country'].str.lower() == filters['country'].lower()]
        
        if filters.get('min_rating'):
            filtered_df = filtered_df[filtered_df['points'] >= float(filters['min_rating'])]
        
        return filtered_df

    def get_unique_countries(self):
        """Get list of unique countries."""
        return sorted(self.df['country'].unique().tolist())

    def get_unique_provinces(self, country=None):
        """Get list of unique provinces for a given country."""
        if country:
            return sorted(self.df[self.df['country'].str.lower() == country.lower()]['province'].unique().tolist())
        return sorted(self.df['province'].unique().tolist())

    def get_unique_varieties(self):
        """Get list of unique wine varieties."""
        return sorted(self.df['variety'].unique().tolist())

    def get_unique_tasters(self):
        """Get list of unique tasters."""
        return sorted(self.df['taster_name'].unique().tolist()) 