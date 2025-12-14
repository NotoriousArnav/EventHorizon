from rest_framework import serializers
from .models import Event, Registration
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]


class EventSerializer(serializers.ModelSerializer):
    organizer = UserSerializer(read_only=True)
    is_registered = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = [
            "id",
            "title",
            "description",
            "start_time",
            "end_time",
            "location",
            "capacity",
            "organizer",
            "created_at",
            "updated_at",
            "is_registered",
        ]
        read_only_fields = ["organizer", "created_at", "updated_at"]

    def get_is_registered(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return Registration.objects.filter(
                event=obj, participant=request.user
            ).exists()
        return False


class RegistrationSerializer(serializers.ModelSerializer):
    event_title = serializers.ReadOnlyField(source="event.title")
    participant_info = UserSerializer(source="participant", read_only=True)

    class Meta:
        model = Registration
        fields = [
            "id",
            "event",
            "event_title",
            "participant_info",
            "status",
            "registered_at",
        ]
        read_only_fields = ["participant", "status", "registered_at", "event"]
