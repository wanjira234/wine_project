from ..common.base import db
from ..common.enums import (
    ExperienceLevel, DrinkingFrequency, WineType, BodyType,
    SweetnessLevel, Currency
)
from sqlalchemy.types import JSON

class UserPreference(db.Model):
    """User preferences model for wine recommendations."""
    
    __tablename__ = 'user_preferences'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    # Account Information is stored in User model
    
    # Wine Experience (Step 2)
    wine_experience = db.Column(JSON, default={
        'experience_level': ExperienceLevel.BEGINNER,
        'drinking_frequency': DrinkingFrequency.OCCASIONALLY,
        'wine_types': []  # Selected wine types
    })

    # Wine Style (Step 3)
    wine_style = db.Column(JSON, default={
        'body_preference': BodyType.MEDIUM,
        'sweetness_level': SweetnessLevel.DRY,
        'price_ranges': {
            'regular': {
                'min': 15,
                'max': 50,
                'currency': Currency.USD
            },
            'special': {
                'min': 50,
                'max': 200,
                'currency': Currency.USD
            }
        }
    })

    # Wine Traits (Step 4)
    wine_traits = db.Column(JSON, default={
        'preferred_traits': []  # Selected wine characteristics
    })

    # Wine Regions (Step 5)
    wine_regions = db.Column(JSON, default={
        'preferred_regions': []  # Selected wine regions
    })

    def __init__(self, user_id):
        self.user_id = user_id

    def update_preferences(self, preference_type, new_preferences):
        """Update specific preference type with new values."""
        current_prefs = getattr(self, preference_type, {})
        if isinstance(current_prefs, dict) and isinstance(new_preferences, dict):
            current_prefs.update(new_preferences)
            setattr(self, preference_type, current_prefs)
            self.save()



    def save(self):
        """Save changes to database."""
        db.session.add(self)
        db.session.commit()

    def to_dict(self):
        """Convert preferences to dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'wine_experience': self.wine_experience,
            'wine_style': self.wine_style,
            'wine_traits': self.wine_traits,
            'wine_regions': self.wine_regions
        }

    def from_signup_data(self, data):
        """
        Create preferences from signup form data.
        
        Args:
            data (dict): The form data from signup
        """
        self.wine_experience = {
            'experience_level': data.get('experience_level', ExperienceLevel.BEGINNER),
            'drinking_frequency': data.get('drinking_frequency', DrinkingFrequency.OCCASIONALLY),
            'wine_types': data.get('wine_types', [])
        }
        
        self.wine_style = {
            'body_preference': data.get('body_preference', BodyType.MEDIUM),
            'sweetness_level': data.get('sweetness_level', SweetnessLevel.DRY),
            'price_ranges': {
                'regular': {
                    'min': float(data.get('regular_budget_min', 15)),
                    'max': float(data.get('regular_budget_max', 50)),
                    'currency': Currency.USD
                },
                'special': {
                    'min': float(data.get('special_budget_min', 50)),
                    'max': float(data.get('special_budget_max', 200)),
                    'currency': Currency.USD
                }
            }
        }
        
        self.wine_traits = {
            'preferred_traits': data.get('wine_traits', [])
        }
        
        self.wine_regions = {
            'preferred_regions': data.get('wine_regions', [])
        }
        
        self.save() 