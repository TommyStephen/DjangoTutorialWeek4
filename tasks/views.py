from rest_framework import generics, permissions
from django.contrib.auth.models import User

from .permissions import IsOwnerOrReadOnly
from .serializers import RegisterSerializer, UserSerializer
from .models import Product, Task
from .serializers import ProductSerializer
from rest_framework import viewsets, permissions

from .serializers import TaskSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # Add permissions for action-specific control
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        # Attach the logged-in user (self.request.user) to the owner field before saving.
        # If you don’t override this method, DRF will just call serializer.save() by default.
        serializer.save(owner=self.request.user)

    # If you want users to only see their own tasks in the list, update get_queryset
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Task.objects.filter(owner=user)
        else:
            return Task.objects.none()  # Return empty queryset for anonymous users

class UserViewSet(viewsets.ReadOnlyModelViewSet):  # Only GET is allowed
    queryset = User.objects.all()
    serializer_class = UserSerializer
