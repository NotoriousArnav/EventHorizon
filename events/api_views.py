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

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Event, Registration
from .serializers import EventSerializer, RegistrationSerializer


class IsOrganizerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow organizers of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the organizer of the event.
        return obj.organizer == request.user


class EventViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows events to be viewed or edited.
    """

    queryset = Event.objects.all().order_by("-start_time")
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOrganizerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)

    @action(
        detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated]
    )
    def register(self, request, pk=None):
        """Register the current user for an event"""
        event = self.get_object()
        user = request.user

        # Check if already registered
        if Registration.objects.filter(event=event, participant=user).exists():
            return Response(
                {"detail": "You are already registered for this event."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Check capacity
        current_registrations = Registration.objects.filter(
            event=event, status="registered"
        ).count()
        if current_registrations >= event.capacity:
            return Response(
                {"detail": "This event is at full capacity."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Create registration
        registration = Registration.objects.create(
            event=event,
            participant=user,
            status="registered",
            answers=request.data.get("answers", {}),
        )

        serializer = RegistrationSerializer(registration)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(
        detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated]
    )
    def unregister(self, request, pk=None):
        """Unregister the current user from an event"""
        event = self.get_object()
        user = request.user

        try:
            registration = Registration.objects.get(event=event, participant=user)
            registration.delete()
            return Response(
                {"detail": "Successfully unregistered from the event."},
                status=status.HTTP_204_NO_CONTENT,
            )
        except Registration.DoesNotExist:
            return Response(
                {"detail": "You are not registered for this event."},
                status=status.HTTP_404_NOT_FOUND,
            )

    @action(
        detail=True, methods=["get"], permission_classes=[permissions.IsAuthenticated]
    )
    def registrations(self, request, pk=None):
        """Get all registrations for an event (organizer only)"""
        event = self.get_object()

        # Only organizer can view registrations
        if event.organizer != request.user:
            return Response(
                {"detail": "Only the event organizer can view registrations."},
                status=status.HTTP_403_FORBIDDEN,
            )

        registrations = Registration.objects.filter(event=event).order_by(
            "-registered_at"
        )
        serializer = RegistrationSerializer(registrations, many=True)
        return Response(serializer.data)


class RegistrationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint to view user's own registrations.
    """

    serializer_class = RegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Return registrations for the current user only"""
        return Registration.objects.filter(participant=self.request.user).order_by(
            "-registered_at"
        )
