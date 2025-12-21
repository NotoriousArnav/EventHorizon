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

from django.views.generic import TemplateView
from django.http import JsonResponse
from django.db import connection
from events.models import Event
from django.utils import timezone
import datetime


class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["upcoming_events"] = Event.objects.filter(
            start_time__gte=timezone.now()
        ).order_by("start_time")[:3]
        return context


def health_check(request):
    """
    Health check endpoint for monitoring services (UptimeRobot, etc.)
    Returns JSON with system status and database connectivity.
    """
    try:
        # Check database connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")

        # Check if we can query the database
        event_count = Event.objects.count()

        return JsonResponse(
            {
                "status": "healthy",
                "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
                "database": "connected",
                "service": "Event Horizon",
                "events_count": event_count,
                "version": "1.0.0",
            }
        )
    except Exception as e:
        return JsonResponse(
            {
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
                "database": "disconnected",
                "service": "Event Horizon",
            },
            status=503,
        )
