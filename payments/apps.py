from django.apps import AppConfig
import json

class PaymentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'payments'

    def ready(self):
        from django_celery_beat.models import PeriodicTask, IntervalSchedule

        # Проверка, существует ли задача
        if not PeriodicTask.objects.filter(name='deactivate_inactive_users').exists():
            schedule, created = IntervalSchedule.objects.get_or_create(
                every=1,
                period=IntervalSchedule.DAYS,
            )
            PeriodicTask.objects.create(
                interval=schedule,
                name='deactivate_inactive_users',
                task='payments.tasks.deactivate_inactive_users',
                kwargs=json.dumps({})
            )
