from .models import User
from .serializers import UserRegistrationSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import (ListCreateAPIView)


class UserProfileListCreateView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    #permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)


