from django.urls import path

from .views import CreateUserView, RetrieveUserView, ProfileViewSet

urlpatterns = [
	path('register/', CreateUserView.as_view()),
	path('user-info/', RetrieveUserView.as_view()),
	path('profile/', ProfileViewSet.as_view({"post": "create", "get": "retrieve", "update": "update"})),
]
