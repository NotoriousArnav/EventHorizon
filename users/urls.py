# Event Horizon - Futuristic Event Management Platform
# Copyright (C) 2025-2026 Arnav Ghosh
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

from django.urls import path, include
from . import views
from .api_views import UserProfileView

urlpatterns = [
    path("profile/", views.profile, name="profile"),
    # OAuth2 Apps Management
    path("oauth2-apps/", views.oauth2_apps, name="oauth2-apps"),
    path("oauth2-apps/create/", views.oauth2_app_create, name="oauth2-app-create"),
    path(
        "oauth2-apps/<int:app_id>/delete/",
        views.oauth2_app_delete,
        name="oauth2-app-delete",
    ),
    # API Keys Management
    path("api-keys/", views.api_keys, name="api-keys"),
    path("api-keys/create/", views.api_key_create, name="api-key-create"),
    path(
        "api-keys/<str:token_id>/delete/", views.api_key_delete, name="api-key-delete"
    ),
    # API
    path("api/me/", UserProfileView.as_view(), name="api-profile-me"),
]
