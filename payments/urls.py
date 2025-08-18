from django.urls import path
from .views import CreateStripeSessionView, StripeSessionStatusAPIView

app_name = 'payments'

urlpatterns = [
    path('create-checkout-session/', CreateStripeSessionView.as_view(), name='create_checkout'),
    path('check-session-status/', StripeSessionStatusAPIView.as_view(), name='check-session-status'),
]





