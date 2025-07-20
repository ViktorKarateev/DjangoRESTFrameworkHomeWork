from django.urls import path, include
from .views import LessonListCreateAPIView, LessonDetailAPIView, CourseViewSet, SubscriptionToggleAPIView
from rest_framework.routers import DefaultRouter


app_name = 'materials'

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')


urlpatterns = [
    path('lessons/', LessonListCreateAPIView.as_view(), name='lesson-list-create'),
    path('lessons/<int:pk>/', LessonDetailAPIView.as_view(), name='lesson-detail'),
    #path('api/users/', include('users.urls')),
    path('subscriptions/toggle/', SubscriptionToggleAPIView.as_view(), name='subscription-toggle'),
]
