from flask_wtf import FlaskForm
from wtforms import SelectField, FloatField, StringField
from wtforms.validators import DataRequired, Optional, NumberRange
from models.common.enums import (
    ExperienceLevel, DrinkingFrequency, WineType, BodyType,
    SweetnessLevel, FlavorIntensity, PriceSensitivity,
    QualityPreference, Currency
)

class UserPreferencesForm(FlaskForm):
    # Wine Knowledge
    experience_level = SelectField(
        'Experience Level',
        choices=[(level.value, level.value.title()) for level in ExperienceLevel],
        validators=[DataRequired()]
    )
    drinking_frequency = SelectField(
        'Drinking Frequency',
        choices=[(freq.value, freq.value.title()) for freq in DrinkingFrequency],
        validators=[DataRequired()]
    )

    # Budget Preferences
    min_price = FloatField(
        'Minimum Price',
        validators=[Optional(), NumberRange(min=0)],
        default=15
    )
    max_price = FloatField(
        'Maximum Price',
        validators=[Optional(), NumberRange(min=0)],
        default=50
    )
    currency = SelectField(
        'Currency',
        choices=[(curr.value, curr.value) for curr in Currency],
        validators=[DataRequired()],
        default=Currency.USD.value
    )
    special_occasion_price = FloatField(
        'Special Occasion Price',
        validators=[Optional(), NumberRange(min=0)],
        default=100
    )

    # Taste Profile
    red_wine_body = SelectField(
        'Red Wine Body',
        choices=[(body.value, body.value.title()) for body in BodyType],
        validators=[DataRequired()],
        default=BodyType.MEDIUM.value
    )
    white_wine_body = SelectField(
        'White Wine Body',
        choices=[(body.value, body.value.title()) for body in BodyType],
        validators=[DataRequired()],
        default=BodyType.MEDIUM.value
    )
    red_wine_sweetness = SelectField(
        'Red Wine Sweetness',
        choices=[(sweet.value, sweet.value.title()) for sweet in SweetnessLevel],
        validators=[DataRequired()],
        default=SweetnessLevel.DRY.value
    )
    white_wine_sweetness = SelectField(
        'White Wine Sweetness',
        choices=[(sweet.value, sweet.value.title()) for sweet in SweetnessLevel],
        validators=[DataRequired()],
        default=SweetnessLevel.OFF_DRY.value
    )
    flavor_intensity = SelectField(
        'Flavor Intensity',
        choices=[(intens.value, intens.value.title()) for intens in FlavorIntensity],
        validators=[DataRequired()],
        default=FlavorIntensity.MEDIUM.value
    )

    # Rating Preferences
    minimum_rating = FloatField(
        'Minimum Rating',
        validators=[Optional(), NumberRange(min=80, max=100)],
        default=88
    )
    price_sensitivity = SelectField(
        'Price Sensitivity',
        choices=[(sens.value, sens.value.title()) for sens in PriceSensitivity],
        validators=[DataRequired()],
        default=PriceSensitivity.MEDIUM.value
    )
    quality_preference = SelectField(
        'Quality Preference',
        choices=[(qual.value, qual.value.title()) for qual in QualityPreference],
        validators=[DataRequired()],
        default=QualityPreference.HIGH.value
    ) 