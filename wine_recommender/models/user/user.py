from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship
from ..common.base import db, BaseModel
from ..common.enums import UserRole
from .preferences import UserPreference
from datetime import datetime
from pprint import pprint

class User(UserMixin, db.Model):
    """User model for authentication and profile management."""
    
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    name = db.Column(db.String(128))
    role = db.Column(db.Enum(UserRole), default=UserRole.CUSTOMER)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_admin = db.Column(db.Boolean, default=False)

    # Relationships
    preferences = db.relationship('UserPreference', backref='user', uselist=False, 
                                cascade='all, delete-orphan', lazy='joined')

    def __init__(self, username, email, name=None, **kwargs):
        super().__init__(**kwargs)
        self.username = username
        self.email = email
        self.name = name or username

    @classmethod
    def create_user(cls, email, password, name=None):
        """Create a new user with default settings."""
        username = cls.generate_unique_username(email)
        user = cls(username=username, email=email, name=name)
        user.set_password(password)
        db.session.add(user)
        db.session.flush()  # This assigns an ID to the user
        
        # Create default preferences after user has an ID
        user.preferences = UserPreference(user_id=user.id)
        user.save()
        return user
    
    def save(self):
        """Save the user to the database."""
        db.session.add(self)
        db.session.commit()

    @classmethod
    def load_user(cls, user_id):
        """Load the most complete version of the user from the DB."""
        return cls.query.filter_by(id=user_id).first()

    @classmethod
    def generate_unique_username(cls, email):
        """Generate a unique username from email."""
        base_username = email.split('@')[0]
        username = base_username
        counter = 1
        
        while cls.query.filter_by(username=username).first():
            username = f"{base_username}{counter}"
            counter += 1
            
        return username

    def set_password(self, password):
        """Set the user's password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check if the provided password matches the user's password."""
        return check_password_hash(self.password_hash, password)
    
    def get_preferences(self, category=None):
        """Get user preferences.
        
        Args:
            category (str, optional): Specific preference category to retrieve.
                                    If None, returns all preferences.
        
        Returns:
            dict: User preferences for the specified category or all preferences.
        """
        try:
            # retrieves user preferences from the database
            pref_from_db = self.query.filter_by(id=self.id).one().preferences.__dict__
            #pprint({k: v for k, v in pref_from_db.items() if not k.startswith('_')})
            return {
                'experience': pref_from_db.get('wine_experience'),
                'wine_types': pref_from_db.get('wine_experience').get('wine_types'),
                'wine_style': pref_from_db.get('wine_style'),
                'wine_traits': pref_from_db.get('wine_traits').get('preferred_traits'),
                'wine_regions': pref_from_db.get('wine_regions').get('preferred_regions')
            }

        except Exception as e:
            print("EXCEPTION IN get_preferences call (User model):  {}".format(e))

        if not self.preferences:
            # this means the user didn't give any preferences
            return {} if category else {'experience': {}, 'wine_types': {}, 
                                      'taste': {}, 'regions': {}, 'budget': {}}
    
        # disabled these specifications for category for now. consider enabling
        '''if category == 'experience':
            return self.preferences.wine_experience or {}
        elif category == 'wine_types':
            return self.preferences.wine_style.get('types', {}) if self.preferences.wine_style else {}
        elif category == 'taste':
            return self.preferences.wine_traits or {}
        elif category == 'regions':
            return self.preferences.wine_regions or {}
        elif category == 'budget':
            return self.preferences.wine_style.get('budget', {}) if self.preferences.wine_style else {}'''
        return {
            'experience': self.preferences.wine_experience or {},
            'wine_types': self.preferences.wine_style.get('types', {}) if self.preferences.wine_style else {},
            'taste': self.preferences.wine_traits or {},
            'regions': self.preferences.wine_regions or {},
            'budget': self.preferences.wine_style.get('budget', {}) if self.preferences.wine_style else {}
        }


    '''def get_preferences(self, category=None):
        """Get user preferences.
        
        Args:
            category (str, optional): Specific preference category to retrieve.
                                    If None, returns all preferences.
        
        Returns:
            dict: User preferences for the specified category or all preferences.
        """
        if not self.preferences:
            return {} if category else {'experience': {}, 'wine_types': {}, 
                                      'taste': {}, 'regions': {}, 'budget': {}}
        if category == 'experience':
            return self.preferences.wine_experience or {}
        elif category == 'wine_types':
            return self.preferences.wine_style.get('types', {}) if self.preferences.wine_style else {}
        elif category == 'taste':
            return self.preferences.wine_traits or {}
        elif category == 'regions':
            return self.preferences.wine_regions or {}
        elif category == 'budget':
            return self.preferences.wine_style.get('budget', {}) if self.preferences.wine_style else {}
        return {
            'experience': self.preferences.wine_experience or {},
            'wine_types': self.preferences.wine_style.get('types', {}) if self.preferences.wine_style else {},
            'taste': self.preferences.wine_traits or {},
            'regions': self.preferences.wine_regions or {},
            'budget': self.preferences.wine_style.get('budget', {}) if self.preferences.wine_style else {}
        }'''

    def update_preferences(self, category, data):
        """Update user preferences for a specific category.
        
        Args:
            category (str): The preference category to update
            data: The new preference data for the category
        """
        if not self.preferences:
            self.preferences = UserPreference(user_id=self.id)
            db.session.add(self.preferences)
        
        self.preferences.update_preferences(category, data)
        
        try:
            db.session.commit()
        except:
            db.session.rollback()
            raise

    def delete_preferences(self, category=None):
        """Delete user preferences.
        
        Args:
            category (str, optional): Specific preference category to delete.
                                    If None, deletes all preferences.
        """
        if not self.preferences:
            return
            
        if category:
            if category == 'experience':
                self.preferences.wine_experience = None
            elif category == 'wine_types':
                if self.preferences.wine_style:
                    self.preferences.wine_style['types'] = None
            elif category == 'taste':
                self.preferences.wine_traits = None
            elif category == 'regions':
                self.preferences.wine_regions = None
            elif category == 'budget':
                if self.preferences.wine_style:
                    self.preferences.wine_style['budget'] = None
        else:
            db.session.delete(self.preferences)
        
        try:
            db.session.commit()
        except:
            db.session.rollback()
            raise

    def to_dict(self):
        """Convert user to dictionary."""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'name': self.name,
            'role': self.role.value if self.role else None,
            'preferences': self.get_preferences()
        }

    def __repr__(self):
        return f'<User {self.username}>' 