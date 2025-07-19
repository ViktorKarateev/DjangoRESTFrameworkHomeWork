from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserProfileUpdateView, PaymentViewSet, UserRegisterAPIView, UserViewSet

app_name = 'users'

router = DefaultRouter()
router.register(r'payments', PaymentViewSet, basename='payment')
router.register(r'users', UserViewSet, basename='customuser')

urlpatterns = [
    path('profile/', UserProfileUpdateView.as_view(), name='user-profile'),
    path('', include(router.urls)),
    path('register/', UserRegisterAPIView.as_view(), name='user-register'),
]
