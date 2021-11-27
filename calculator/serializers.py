from rest_framework import serializers
from django.contrib.auth import get_user_model  # If used custom user model
from rest_framework_simplejwt.tokens import RefreshToken

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)
    access_token = serializers.SerializerMethodField()

    def create(self, validated_data):

        user = UserModel.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
        )
        return user

    class Meta:
        model = UserModel
        fields = ("id", "username", "password", "access_token", )

    def get_access_token(self, obj):
        return str(RefreshToken.for_user(obj).access_token)