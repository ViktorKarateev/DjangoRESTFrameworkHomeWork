from rest_framework import viewsets, filters, generics, permissions
from django_filters.rest_framework import DjangoFilterBackend
from .models import Payment, CustomUser
from .serializers import UserProfileSerializer, UserRegisterSerializer, PaymentSerializer,  UserLimitedSerializer
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserRegisterAPIView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]



class PaymentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['course', 'lesson', 'payment_method']
    ordering_fields = ['payment_date']
    ordering = ['-payment_date']


class UserProfileUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user_id = self.kwargs.get('pk')
        if user_id:
            user = CustomUser.objects.filter(pk=user_id).first()
            if not user:
                raise PermissionDenied("Пользователь не найден")
            return user
        return self.request.user

    def get_serializer_class(self):
        if self.get_object() != self.request.user:
            return UserLimitedSerializer
        return UserProfileSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH']:
            if self.get_object() != self.request.user:
                raise PermissionDenied("Вы не можете редактировать чужой профиль")
        return super().get_permissions()