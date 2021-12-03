from rest_framework import serializers
from django.contrib.auth import get_user_model  # If used custom user model
from rest_framework_simplejwt.tokens import RefreshToken
from calculator.models import (
    Profile,
    PhysicalActivity,
    EatingCategory,
    FoodCategory,
    FoodItem,
    WaterEvent,
    FoodEvent,
)

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)
    access_token = serializers.SerializerMethodField()
    is_ready = serializers.SerializerMethodField()

    def create(self, validated_data):

        user = UserModel.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
        )
        return user

    class Meta:
        model = UserModel
        fields = ("id", "username", "password", "access_token", "is_ready")

    def get_access_token(self, obj):
        return str(RefreshToken.for_user(obj).access_token)

    def get_is_ready(self, obj):
        return bool(Profile.objects.filter(user_id=obj.id).first())


class PhysicalActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = PhysicalActivity
        fields = "__all__"


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True, required=False)

    birth_date = serializers.DateField(required=False)
    sex = serializers.CharField(required=False)
    physical_activity = serializers.PrimaryKeyRelatedField(
        queryset=PhysicalActivity.objects.all(), required=False
    )

    def create(self, validated_data):

        profile = Profile.objects.create(
            user_id=validated_data["user_id"],
            weight=validated_data["weight"],
            height=validated_data["height"],
            birth_date=validated_data["birth_date"],
            sex=validated_data["sex"],
            physical_activity_id=validated_data["physical_activity"].id,
        )
        profile.save()
        return profile

    class Meta:
        model = Profile
        fields = "__all__"


class EatingCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = EatingCategory
        fields = "__all__"


class FoodCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodCategory
        fields = "__all__"


class FoodItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodItem
        fields = "__all__"


class WaterEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = WaterEvent
        fields = "__all__"


class FoodEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodEvent
        fields = "__all__"


class CommentSerializer(serializers.Serializer):
    calories = serializers.IntegerField()
    fats = serializers.IntegerField()
    protein = serializers.IntegerField()
    carbohydrate = serializers.IntegerField()
