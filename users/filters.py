import django_filters
from .models import Payment

class PaymentFilter(django_filters.FilterSet):
    class Meta:
        model = Payment
        fields = {
            'course': ['exact'],
            'lesson': ['exact'],
            'payment_method': ['exact'],
            'payment_date': ['exact', 'gte', 'lte'],  # необязательно, но можно
        }
