from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from models.user.user import User

class RegistrationForm(FlaskForm):
    """Form for user registration."""
    
    email = StringField('Email', validators=[
        DataRequired(message='Email is required'),
        Email(message='Please enter a valid email address')
    ])
    
    password = PasswordField('Password', validators=[
        DataRequired(message='Password is required'),
        Length(min=8, message='Password must be at least 8 characters long')
    ])
    
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(message='Please confirm your password'),
        EqualTo('password', message='Passwords must match')
    ])
    
    name = StringField('Name', validators=[
        DataRequired(message='Name is required'),
        Length(max=128, message='Name must be less than 128 characters')
    ])
    
    bio = TextAreaField('Bio', validators=[
        Length(max=500, message='Bio must be less than 500 characters')
    ])
    
    submit = SubmitField('Register')
    
    def validate_email(self, email):
        """Check if email is already registered."""
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered. Please use a different email.')

class LoginForm(FlaskForm):
    """Form for user login."""
    email = StringField('Email', 
                       validators=[
                           DataRequired(message="Email is required"),
                           Email(message="Please enter a valid email address"),
                           Length(max=120)
                       ])
    password = PasswordField('Password',
                           validators=[
                               DataRequired(message="Password is required")
                           ])
    remember = BooleanField('Remember me') 