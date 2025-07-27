from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_course_update_email(recipient_email, course_name):
    subject = f"Обновление курса: {course_name}"
    message = f"Здравствуйте!\n\nКурс '{course_name}' был обновлён. Проверьте новые материалы."
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [recipient_email]

    send_mail(subject, message, from_email, recipient_list)