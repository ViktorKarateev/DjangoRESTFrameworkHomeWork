from django.urls import path, include
from .views import LessonListCreateAPIView, LessonDetailAPIView

app_name = 'materials'

urlpatterns = [
    path('lessons/', LessonListCreateAPIView.as_view(), name='lesson-list-create'),
    path('lessons/<int:pk>/', LessonDetailAPIView.as_view(), name='lesson-detail'),
    path('api/users/', include('users.urls')),

]
