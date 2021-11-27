from rest_framework import permissions, viewsets, status
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from django.contrib.auth import get_user_model # If used custom user model
from rest_framework.response import Response

from .models import Profile
from .serializers import UserSerializer, ProfileSerializer


class CreateUserView(CreateAPIView):

    model = get_user_model()
    permission_classes = [
        permissions.AllowAny    # Or anon users can't register
    ]
    serializer_class = UserSerializer


class RetrieveUserView(RetrieveAPIView):
    model = get_user_model()
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        return Response(self.get_serializer(request.user).data)


class ProfileViewSet(viewsets.ModelViewSet):
    model = Profile
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = ProfileSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        if Profile.objects.filter(user=user):
            return Response({"message": "User already has profile"})
        validated_data = serializer.validated_data
        validated_data["user_id"] = user.id
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
