from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from datetime import timedelta
from django.utils import timezone
from users.models import CustomUser
import logging

logger = logging.getLogger(__name__)

@shared_task
def send_course_update_email(recipient_email, course_name):
    subject = f"Обновление курса: {course_name}"
    message = f"Здравствуйте!\n\nКурс '{course_name}' был обновлён. Проверьте новые материалы."
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [recipient_email]

    send_mail(subject, message, from_email, recipient_list)


@shared_task
def deactivate_inactive_users():
    threshold_date = timezone.now() - timedelta(days=30)
    inactive_users = CustomUser.objects.filter(last_login__lt=threshold_date, is_active=True)

    count = inactive_users.update(is_active=False)
    logger.info(f"{count} пользователей было деактивировано за неактивность более 30 дней.")

