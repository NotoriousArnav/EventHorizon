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

from rest_framework import serializers
from .models import Event, Registration
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name"]


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
            "slug",
        ]
        read_only_fields = ["organizer", "created_at", "updated_at", "slug"]

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
