from django.db import models
from django.contrib.auth.models import AbstractUser
from apps.authentication.validators import validate_uzb_phone_number
from django.utils import timezone
import random
import string
from apps.authentication.tasks import send_background_sms


class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True, validators=[validate_uzb_phone_number])
    full_name = models.CharField(max_length=70)
    
    def __str__(self):
        try:
            return self.get_full_name()
        except:
            return self.username
    
    def get_full_name(self):
        return self.full_name
        

class PhoneToken(models.Model):
    phone_number = models.CharField(max_length=20, validators=[validate_uzb_phone_number])
    token = models.CharField(max_length=6, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now, null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.phone_number

    class Meta:
        verbose_name = "Sms token"
        verbose_name_plural = "Sms Tokens"

    def __str__(self):
        return "{} - {}".format(self.phone_number, self.token)
    
    @property
    def is_expired(self):
        return self.expires_at < timezone.now()

    @classmethod
    def verify_token(cls, phone_number, token):
        try:
            phone_token = cls.objects.filter(phone_number=phone_number).last()
            if phone_token.token == token and phone_token.expires_at > timezone.now():
                return True
            return False
        except cls.DoesNotExist:
            return False
    
    @classmethod
    def generate_token(cls, phone_number):
        phone_token = cls.objects.create(phone_number=phone_number)
        token = ''.join(random.choices(string.digits, k=6))
        phone_token.token = token
        phone_token.expires_at = timezone.now() + timezone.timedelta(minutes=3)
        phone_token.save()
        message = "Sizning tokeningiz: {}".format(token)
        send_background_sms.apply_async((phone_number, message))
        return phone_token.token
    