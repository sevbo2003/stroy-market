from celery import shared_task
from core.sms.eskiz import eskiz


@shared_task
def send_background_sms(phone_number, message):
    try:
        eskiz.send_sms(str(phone_number)[1:], message, from_whom='4546')
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": e}