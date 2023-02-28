from apps.authentication.models import PhoneToken
import random
import string
from django.utils import timezone
from apps.authentication.tasks import send_background_sms


def generate_token(phone_number):
    phone_token = PhoneToken.objects.create(phone_number=phone_number)
    token = ''.join(random.choices(string.digits, k=6))
    phone_token.token = token
    phone_token.expires_at = timezone.now() + timezone.timedelta(minutes=3)
    phone_token.save()
    message = "Sizning maxsus kodiz: {}".format(token)
    send_background_sms.apply_async((phone_number, message))
    return phone_token.token


def verify_token(phone_number, token):
    try:
        phone_token = PhoneToken.objects.filter(phone_number=phone_number).last()
        if phone_token.token == token and phone_token.expires_at > timezone.now():
            return True
        return False
    except PhoneToken.DoesNotExist:
        return False