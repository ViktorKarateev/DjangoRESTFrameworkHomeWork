from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserProfileUpdateView, PaymentViewSet

app_name = 'users'

router = DefaultRouter()
router.register(r'payments', PaymentViewSet, basename='payment')

urlpatterns = [
    path('profile/', UserProfileUpdateView.as_view(), name='user-profile'),
    path('', include(router.urls)),
]
