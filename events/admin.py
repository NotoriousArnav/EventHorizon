from django.contrib import admin
from .models import Event, Registration


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "organizer",
        "start_time",
        "end_time",
        "location",
        "capacity",
    )
    search_fields = ("title", "description", "location")
    list_filter = ("start_time", "created_at")


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ("event", "participant", "status", "registered_at")
    list_filter = ("status", "registered_at")
    search_fields = ("event__title", "participant__username", "participant__email")
