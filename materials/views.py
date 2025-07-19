from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModerator, IsOwner


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated & IsOwner]
        elif self.action in ['retrieve', 'list']:
            permission_classes = [IsAuthenticated | IsModerator]
        elif self.action == 'create':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListCreateAPIView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]  # Только авторизованные (без модераторов)
        return [IsAuthenticated() | IsModerator()]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'GET']:
            return [IsAuthenticated() | IsModerator()]
        elif self.request.method == 'DELETE':
            return [IsAuthenticated()]  # Только авторизованные, не модераторы
        return [IsAuthenticated()]
