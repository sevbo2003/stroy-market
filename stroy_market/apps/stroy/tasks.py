from celery import shared_task
from core.sms.eskiz import eskiz
# from apps.stroy.models import Newsletter


@shared_task
def send_news(numbers,message):
    try:
        for i in numbers:
            eskiz.send_sms(str(i)[1:], message, from_whom='4546')
        return {"status": "success", "message": "Xabar muvaffaqiyatli yuborildi"}
    except Exception as e:
        return {"status": "error", "message": e}
    