from django.urls import path

from .views import CreateUserView, RetrieveUserView, ProfileViewSet, PhysicalActivityViewSet, EatingCategoryViewSet, \
	FoodCategoryViewSet, WaterEventViewSet

urlpatterns = [
	path('register/', CreateUserView.as_view()),
	path('user-info/', RetrieveUserView.as_view()),
	path('profile/', ProfileViewSet.as_view({"post": "create", "get": "retrieve", "patch": "update"})),
	path('physical-activity/', PhysicalActivityViewSet.as_view({"get": "list", })),
	path('eating-category/', EatingCategoryViewSet.as_view({"get": "list", })),
	path('food-category/', FoodCategoryViewSet.as_view({"get": "list", })),
	path('water-event/', WaterEventViewSet.as_view({"get": "list", "post": "create"})),
]
