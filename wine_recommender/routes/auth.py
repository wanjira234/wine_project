from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, login_required, current_user
from forms.auth import RegistrationForm, LoginForm
from models.user.user import User
from models.user.preferences import UserPreference
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db
from models.common.enums import (
    ExperienceLevel, DrinkingFrequency, WineType, BodyType, 
    SweetnessLevel, FlavorIntensity, WineTrait, WineTraitCategory,
    WineRegion
)
import pycountry
from models.order import Order
from models.order_item import OrderItem

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password_hash, password):
            flash('Please check your login details and try again.')
            return redirect(url_for('auth.login'))

        login_user(user, remember=remember)
        return redirect(url_for('main.profile'))

    return render_template('auth/login.html')

def get_trait_icon(trait):
    """Get the appropriate Font Awesome icon for a wine trait."""
    icon_map = {
        # Taste traits
        'sweet': 'candy-cane',
        'dry': 'wine-glass-empty',
        'tart': 'lemon',
        'crisp': 'snowflake',
        'tangy': 'bolt',
        'juicy': 'tint',
        'rich': 'crown',
        'smooth': 'water',
        'soft': 'feather',
        'sharp': 'angle-double-right',

        # Aroma traits
        'almond': 'seedling',
        'apple': 'apple-alt',
        'berry': 'apple-alt',
        'citrus': 'lemon',
        'peach': 'apple-alt',
        'vanilla': 'leaf',
        'chocolate': 'cookie',
        'coffee': 'coffee',
        'caramel': 'cookie-bite',
        'honey': 'honey-pot',
        'spice': 'pepper-hot',
        'cinnamon': 'mortar-pestle',
        'nutmeg': 'mortar-pestle',
        'pepper': 'pepper-hot',

        # Body traits
        'light_bodied': 'feather',
        'medium_bodied': 'balance-scale',
        'full_bodied': 'wine-glass',
        'dense': 'cube',
        'thick': 'layer-group',
        'robust': 'dumbbell',
        'hearty': 'heart',

        # Character traits
        'complex': 'puzzle-piece',
        'elegant': 'crown',
        'fresh': 'leaf',
        'vibrant': 'sun',
        'bright': 'star',
        'powerful': 'bolt',
        'concentrated': 'compress',
        'refined': 'gem',

        # Additional notes
        'floral': 'flower',
        'herbal': 'seedling',
        'earthy': 'mountain',
        'mineral': 'gem',
        'oak': 'tree',
        'smoke': 'smoke',
        'leather': 'shoe-prints',
        'tobacco': 'smoking',
        'cedar': 'tree'
    }
    return icon_map.get(trait, 'wine-glass')  # Default to wine-glass if trait not found

def get_trait_categories():
    """Organize wine traits by category."""
    return {
        'Taste': [trait.value for trait in WineTrait if trait.value in [
            'sweet', 'dry', 'tart', 'crisp', 'tangy', 'juicy', 'rich', 'smooth', 'soft', 'sharp'
        ]],
        'Aroma': [trait.value for trait in WineTrait if trait.value in [
            'almond', 'apple', 'berry', 'citrus', 'peach', 'vanilla', 'chocolate', 'coffee',
            'caramel', 'honey', 'spice', 'cinnamon', 'nutmeg', 'pepper'
        ]],
        'Body': [trait.value for trait in WineTrait if trait.value in [
            'light_bodied', 'medium_bodied', 'full_bodied', 'dense', 'thick', 'robust', 'hearty'
        ]],
        'Character': [trait.value for trait in WineTrait if trait.value in [
            'complex', 'elegant', 'fresh', 'vibrant', 'bright', 'powerful', 'concentrated', 'refined'
        ]],
        'Additional Notes': [trait.value for trait in WineTrait if trait.value in [
            'floral', 'herbal', 'earthy', 'mineral', 'oak', 'smoke', 'leather', 'tobacco', 'cedar'
        ]]
    }

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user:
            flash('Email address already exists')
            return redirect(url_for('auth.signup'))

        new_user = User.create_user(email=email, name=name, password=password)

        return redirect(url_for('auth.login'))

    return render_template('auth/signup.html')

def get_experience_description(level):
    """Get description for each experience level."""
    descriptions = {
        ExperienceLevel.BEGINNER: "New to wine or just starting to explore different varieties",
        ExperienceLevel.INTERMEDIATE: "Familiar with common varieties and basic wine characteristics",
        ExperienceLevel.EXPERT: "Deep knowledge of wine production, regions, and fine distinctions"
    }
    return descriptions.get(level, "")

def get_frequency_description(frequency):
    """Get description for each drinking frequency."""
    descriptions = {
        DrinkingFrequency.RARELY: "A few times a year on special occasions",
        DrinkingFrequency.OCCASIONALLY: "Once or twice a month",
        DrinkingFrequency.REGULARLY: "About once a week",
        DrinkingFrequency.FREQUENTLY: "Several times a week"
    }
    return descriptions.get(frequency, "")

def format_display_name(value):
    """Format enum values into display-friendly names."""
    if not value:
        return ""
    return value.replace('_', ' ').title()

def get_wine_type_icon(wine_type):
    """Get Font Awesome icon and color class for each wine type."""
    icons = {
        WineType.RED: {
            'icon': 'fa-wine-bottle',
            'color': 'text-danger'
        },
        WineType.WHITE: {
            'icon': 'fa-wine-bottle',
            'color': 'text-warning'
        },
        WineType.ROSE: {
            'icon': 'fa-wine-bottle',
            'color': 'text-pink'
        },
        WineType.SPARKLING: {
            'icon': 'fa-glass-cheers',
            'color': 'text-warning'
        },
        WineType.DESSERT: {
            'icon': 'fa-wine-glass',
            'color': 'text-amber'
        }
    }
    default = {'icon': 'fa-wine-bottle', 'color': 'text-muted'}
    return icons.get(wine_type, default)

@auth.route('/signup/review', methods=['GET'])
def review_signup():
    form_data = session.get('signup_data')
    if not form_data:
        flash('Please fill out the signup form first.', 'warning')
        return redirect(url_for('auth.signup'))
    
    # Format the display values for the review page
    formatted_data = {
        **form_data,
        'experience_level': format_display_name(form_data.get('experience_level')),
        'drinking_frequency': format_display_name(form_data.get('drinking_frequency')),
        'body_preference': format_display_name(form_data.get('body_preference')),
        'sweetness_level': format_display_name(form_data.get('sweetness_level')),
        'wine_types': [format_display_name(wt) for wt in form_data.getlist('wine_types')] if form_data.getlist('wine_types') else [],
        'wine_regions': [format_display_name(wr) for wr in form_data.getlist('wine_regions')] if form_data.getlist('wine_regions') else []
    }
        
    return render_template('auth/review.html',
                         form_data=formatted_data,
                         get_trait_icon=get_trait_icon)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@auth.route('/forgot-password')
def forgot_password():
    # Placeholder for password reset functionality
    flash('Password reset functionality is not yet implemented.', 'info')
    return redirect(url_for('auth.login'))

@auth.route('/delete_account', methods=['POST'])
@login_required
def delete_account():
    # Verify password
    password = request.form.get('password')
    if not password or not current_user.check_password(password):
        flash('Incorrect password. Please try again.', 'danger')
        return redirect(url_for('main.profile'))
    
    try:
        # Get user ID before logout
        user_id = current_user.id
        
        # Logout the user first
        logout_user()
        
        # Delete user data
        user = User.query.get(user_id)
        if user:
            # Delete related data first (preferences, orders, etc.)
            if hasattr(user, 'preferences'):
                db.session.delete(user.preferences)
            
            # Delete orders if they exist
            Order.query.filter_by(user_id=user_id).delete()
            
            # Delete the user
            db.session.delete(user)
            db.session.commit()
            
            flash('Your account has been successfully deleted.', 'success')
        
        return redirect(url_for('main.index'))
        
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while deleting your account. Please try again.', 'danger')
        return redirect(url_for('main.profile')) 