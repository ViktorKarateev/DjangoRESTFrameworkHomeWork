from django.urls import path
from .views import CreateStripeSessionView

app_name = 'payments'

urlpatterns = [
    path('create-checkout-session/', CreateStripeSessionView.as_view(), name='create_checkout'),
]
