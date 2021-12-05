from django.urls import path

from .views import (
    CreateUserView,
    RetrieveUserView,
    ProfileViewSet,
    PhysicalActivityViewSet,
    EatingCategoryViewSet,
    FoodCategoryViewSet,
    WaterEventViewSet,
    FoodItemViewSet,
    FoodEventViewSet,
    StatisticsView,
)
#init base endpoints
urlpatterns = [
    path("register/", CreateUserView.as_view()),
    path("user-info/", RetrieveUserView.as_view()),
    path(
        "profile/",
        ProfileViewSet.as_view(
            {"post": "create", "get": "retrieve", "patch": "update"}
        ),
    ),
    path(
        "physical-activity/",
        PhysicalActivityViewSet.as_view(
            {
                "get": "list",
            }
        ),
    ),
    path(
        "eating-category/",
        EatingCategoryViewSet.as_view(
            {
                "get": "list",
            }
        ),
    ),
    path(
        "food-category/",
        FoodCategoryViewSet.as_view(
            {
                "get": "list",
            }
        ),
    ),
    path(
        "food-item/",
        FoodItemViewSet.as_view(
            {
                "get": "list",
            }
        ),
    ),
    path("water-event/", WaterEventViewSet.as_view({"get": "list", "post": "create"})),
    path("food-event/", FoodEventViewSet.as_view({"get": "list", "post": "create"})),
    path("statistics/", StatisticsView.as_view()),
]
