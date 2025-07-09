from django.urls import path
from .views import UserProfileUpdateView

app_name = 'users'

urlpatterns = [
    path('profile/', UserProfileUpdateView.as_view(), name='user-profile'),
]
