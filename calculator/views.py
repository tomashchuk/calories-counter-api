from itertools import chain

from django.db.models import Sum
from rest_framework import permissions, viewsets, status
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from django.contrib.auth import get_user_model  # If used custom user model
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (
    Profile,
    PhysicalActivity,
    EatingCategory,
    FoodCategory,
    WaterEvent,
    FoodItem,
    FoodEvent,
)
from .serializers import (
    UserSerializer,
    ProfileSerializer,
    PhysicalActivitySerializer,
    EatingCategorySerializer,
    FoodCategorySerializer,
    WaterEventSerializer,
    FoodItemSerializer,
    FoodEventSerializer,
)
from .utils import get_dates_for_today_filtering, get_dates_for_week_filtering


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = "page_size"
    max_page_size = 1000


class CreateUserView(CreateAPIView):

    model = get_user_model()
    permission_classes = [permissions.AllowAny]  # Or anon users can't register
    serializer_class = UserSerializer


class RetrieveUserView(RetrieveAPIView):
    model = get_user_model()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        return Response(self.get_serializer(request.user).data)


class PhysicalActivityViewSet(viewsets.ModelViewSet):
    model = PhysicalActivity
    permission_classes = [permissions.AllowAny]
    serializer_class = PhysicalActivitySerializer
    queryset = PhysicalActivity.objects.all()


class ProfileViewSet(viewsets.ModelViewSet):
    model = Profile
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        if Profile.objects.filter(user=user):
            return Response({"message": "User already has profile"})
        validated_data = serializer.validated_data
        validated_data["user_id"] = user.id
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        # make sure to catch 404's below
        obj = queryset.filter(user_id=self.request.user.id).first()
        self.check_object_permissions(self.request, obj)
        return obj

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)


class EatingCategoryViewSet(viewsets.ModelViewSet):
    model = EatingCategory
    permission_classes = [permissions.AllowAny]
    serializer_class = EatingCategorySerializer
    queryset = EatingCategory.objects.all()


class FoodCategoryViewSet(viewsets.ModelViewSet):
    model = FoodCategory
    permission_classes = [permissions.AllowAny]
    serializer_class = FoodCategorySerializer
    queryset = FoodCategory.objects.all()


class WaterEventViewSet(viewsets.ModelViewSet):
    model = WaterEvent
    permission_classes = [permissions.AllowAny]
    serializer_class = WaterEventSerializer
    queryset = WaterEvent.objects.all()

    def get_queryset(self):

        today_start, today_end = get_dates_for_today_filtering()
        return self.queryset.filter(
            profile=Profile.objects.get(user_id=self.request.user.id),
            created__lte=today_end,
            created__gte=today_start,
        )


class FoodItemViewSet(viewsets.ModelViewSet):
    model = FoodItem
    permission_classes = [permissions.AllowAny]
    serializer_class = FoodItemSerializer
    queryset = FoodItem.objects.all()

    def get_queryset(self):
        category_id = self.request.query_params.get("category_id")
        return self.queryset.filter(category_id=category_id)


class FoodEventViewSet(viewsets.ModelViewSet):
    model = FoodEvent
    permission_classes = [permissions.AllowAny]
    serializer_class = FoodEventSerializer
    queryset = FoodEvent.objects.all()

    def get_queryset(self):
        return self.queryset.filter(
            profile=Profile.objects.get(user_id=self.request.user.id)
        )


class StatisticsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        today_end = None
        start_day = None
        result = None
        period = request.query_params.get("period")
        if period == "today":
            start_day, today_end = get_dates_for_today_filtering()
            result = (
                FoodEvent.objects.values("eating_category_id").filter(
                    profile=Profile.objects.get(user_id=request.user.id),
                    created__lte=today_end,
                    created__gte=start_day,
                ).annotate(
                    Sum("food_item__calorie"),
                    Sum("food_item__fats"),
                    Sum("food_item__protein"),
                    Sum("food_item__carbohydrate"),
                ).order_by()
            )
        elif period == "week":
            start_day, today_end = get_dates_for_week_filtering()
            result_food = (
                FoodEvent.objects.values("created__date").filter(
                    profile=Profile.objects.get(user_id=request.user.id),
                    created__lte=today_end,
                    created__gte=start_day,
                ).annotate(
                    Sum("food_item__calorie"),
                    Sum("food_item__fats"),
                    Sum("food_item__protein"),
                    Sum("food_item__carbohydrate"),
                ).order_by()
            )
            result_water = WaterEvent.objects.values("created__date").filter(
                profile=Profile.objects.get(user_id=request.user.id),
                created__lte=today_end,
                created__gte=start_day,).annotate(Sum("quantity"),)\
                .order_by()
            result = list(chain(result_food, result_water))

        return Response(result)
