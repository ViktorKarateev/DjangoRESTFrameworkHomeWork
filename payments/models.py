from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    course_name = models.CharField(max_length=255)  # или можно ForeignKey на Course, если есть связь
    amount = models.PositiveIntegerField(help_text='Сумма в копейках')
    session_id = models.CharField(max_length=255, unique=True)
    status = models.CharField(max_length=50, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.course_name} — {self.amount / 100:.2f} USD'
