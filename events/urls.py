from django.urls import path
from . import views

urlpatterns = [
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
        "registration/<int:registration_id>/manage/",
        views.ManageRegistrationView.as_view(),
        name="manage-registration",
    ),
    path("my-events/", views.UserEventListView.as_view(), name="user-events"),
]
