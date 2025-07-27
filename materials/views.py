from django.shortcuts import get_object_or_404
from rest_framework import viewsets, generics, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from users.permissions import IsModerator, IsOwner
from .models import Course, Lesson, Subscription
from .paginators import StandardResultsSetPagination
from .serializers import CourseSerializer, LessonSerializer
from payments.tasks import send_course_update_email
from django.utils import timezone
from datetime import timedelta

pagination_class = StandardResultsSetPagination


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = StandardResultsSetPagination

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsOwner]
        elif self.action in ['retrieve', 'list']:
            permission_classes = [IsAuthenticated, IsModerator]
        elif self.action == 'create':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        instance = serializer.save()

        # Проверка: обновлялся ли курс за последние 4 часа
        if timezone.now() - instance.updated_at < timedelta(hours=4):
            return

        subscribers = Subscription.objects.filter(course=instance)
        for sub in subscribers:
            send_course_update_email.delay(sub.user.email, instance.name)


class LessonListCreateAPIView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = StandardResultsSetPagination

    def get_permissions(self):
        if self.request.method == 'POST':
            permission_classes = [IsAuthenticated, ~IsModerator]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH']:
            return [IsAuthenticated(), IsOwner()]
        elif self.request.method == 'GET':
            return [IsAuthenticated(), IsModerator()]
        elif self.request.method == 'DELETE':
            return [IsAuthenticated(), IsOwner()]
        return [IsAuthenticated()]


class SubscriptionToggleSerializer(serializers.Serializer):
    course_id = serializers.IntegerField()


class SubscriptionToggleAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SubscriptionToggleSerializer


    def post(self, request, *args, **kwargs):
        course_id = request.data.get('course_id')
        course = get_object_or_404(Course, id=course_id)
        user = request.user

        subscription = Subscription.objects.filter(user=user, course=course)

        if subscription.exists():
            subscription.delete()
            message = 'подписка удалена'
        else:
            Subscription.objects.create(user=user, course=course)
            message = 'подписка добавлена'

        return Response({'message': message})
