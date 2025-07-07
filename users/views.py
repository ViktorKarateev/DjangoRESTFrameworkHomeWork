from rest_framework import generics, permissions
from .models import CustomUser
from .serializers import UserProfileSerializer


class UserProfileUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.AllowAny]  # позже заменим на IsAuthenticated

    def get_object(self):
        return self.request.user

