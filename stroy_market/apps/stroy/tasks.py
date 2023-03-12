from celery import shared_task
from core.sms.eskiz import eskiz


@shared_task
def send_news(numbers, message):
    try:
        for i in numbers:
            eskiz.send_sms(str(i)[1:], message, from_whom='4546')
            return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": e}
    