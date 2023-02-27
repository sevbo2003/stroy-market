from eskiz_sms import EskizSMS
from django.conf import settings


eskiz = EskizSMS(
            email=settings.ESKIZ_EMAIL,
            password=settings.ESKIZ_PASSWORD,
        )
# eskiz.send_sms(str(number)[1:], message, from_whom='4546')