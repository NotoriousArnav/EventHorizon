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
from rest_framework.routers import DefaultRouter
from . import views
from . import api_views

router = DefaultRouter()
router.register(r"events", api_views.EventViewSet, basename="api-events")
router.register(
    r"registrations", api_views.RegistrationViewSet, basename="api-registrations"
)

urlpatterns = [
    path("api/", include(router.urls)),
    path("events/", views.EventListView.as_view(), name="event-list"),
    path("events/new/", views.EventCreateView.as_view(), name="event-create"),
    path("events/<slug:slug>/", views.EventDetailView.as_view(), name="event-detail"),
    path(
        "events/<slug:slug>/update/",
        views.EventUpdateView.as_view(),
        name="event-update",
    ),
    path(
        "events/<slug:slug>/delete/",
        views.EventDeleteView.as_view(),
        name="event-delete",
    ),
    path(
        "events/<slug:slug>/register/",
        views.EventRegistrationView.as_view(),
        name="event-register",
    ),
    path(
        "events/<slug:slug>/unregister/",
        views.EventUnregistrationView.as_view(),
        name="event-unregister",
    ),
    path(
        "events/<slug:slug>/export/",
        views.EventExportView.as_view(),
        name="event-export",
    ),
    path(
        "events/<slug:slug>/webhooks/new/",
        views.WebhookCreateView.as_view(),
        name="webhook-create",
    ),
    path(
        "webhooks/<int:pk>/edit/",
        views.WebhookUpdateView.as_view(),
        name="webhook-update",
    ),
    path(
        "webhooks/<int:pk>/delete/",
        views.WebhookDeleteView.as_view(),
        name="webhook-delete",
    ),
    path(
        "webhooks/<int:pk>/toggle/",
        views.WebhookToggleActiveView.as_view(),
        name="webhook-toggle",
    ),
    path(
        "registration/<int:registration_id>/manage/",
        views.ManageRegistrationView.as_view(),
        name="manage-registration",
    ),
    path("my-events/", views.UserEventListView.as_view(), name="user-events"),
]
