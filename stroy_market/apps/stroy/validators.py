from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_star_rating(value):
    """
    Validator to check if the input value is a valid star rating with 0.5 step.
    """
    if value not in [i/2 for i in range(1, 11)]:
        raise ValidationError(_('Invalid star rating. Please enter a rating between 0.5 and 5 with 0.5 step.'), code='invalid_rating')
