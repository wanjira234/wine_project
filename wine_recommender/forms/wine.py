from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, FloatField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Optional, NumberRange
from models.common.enums import WineType, WineRegion

class AddWineForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    type = SelectField('Type', choices=[(type.value, type.value.title()) for type in WineType], validators=[DataRequired()])
    region = SelectField('Region', choices=[(region.value, region.value.title()) for region in WineRegion], validators=[DataRequired()])
    year = IntegerField('Year', validators=[Optional()])
    price = FloatField('Price', validators=[DataRequired(), NumberRange(min=0)])
    stock = IntegerField('Stock', validators=[DataRequired(), NumberRange(min=0)])
    description = TextAreaField('Description', validators=[Optional()])
    image_url = StringField('Image URL', validators=[Optional()]) 