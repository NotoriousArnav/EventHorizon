from django.urls import path, include
from . import views
from .api_views import UserProfileView

urlpatterns = [
    path("profile/", views.profile, name="profile"),
    path("api/me/", UserProfileView.as_view(), name="api-profile-me"),
]
