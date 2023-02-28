# uzb phone number validator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re


def validate_uzb_phone_number(value):
    if not re.match(r'^\+998\d{9}$', value):
        raise ValidationError(
            _('%(value)s bu o\'zbekiston telefon raqami emas'),
            params={'value': value},
        )
    