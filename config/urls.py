from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from materials.views import CourseViewSet

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),  #  Добавили router маршруты
    path('api/', include(('materials.urls', 'materials'), namespace='materials')),
    path('api/users/', include(('users.urls', 'users'), namespace='users')),
]
