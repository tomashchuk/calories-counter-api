from rest_framework import serializers
from django.contrib.auth import get_user_model  # If used custom user model
from rest_framework_simplejwt.tokens import RefreshToken
from calculator.models import Profile

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)
    access_token = serializers.SerializerMethodField()
    is_ready = serializers.SerializerMethodField()

    def create(self, validated_data):

        user = UserModel.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
        )
        return user

    class Meta:
        model = UserModel
        fields = ("id", "username", "password", "access_token", "is_ready")

    def get_access_token(self, obj):
        return str(RefreshToken.for_user(obj).access_token)

    def get_is_ready(self, obj):
        return bool(Profile.objects.filter(user_id=obj.id).first())


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def create(self, validated_data):

        profile = Profile.objects.create(
            user_id=validated_data["user_id"],
            width=validated_data['width'],
            height=validated_data['height'],
            birth_date=validated_data['birth_date'],
            sex=validated_data['sex'],
        )
        return profile

    class Meta:
        model = Profile
        fields = '__all__'

    def get_user(self, obj):
        return UserSerializer(obj.user)
