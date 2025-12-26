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
from django.views.generic import TemplateView as PlainTemplateView
from django.http import JsonResponse
from django.db import connection
from django.core.cache import cache
from django.db.models.manager import Manager
from events.models import Event
from typing import cast, Any
from django.utils import timezone
import datetime


class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):  # type: ignore[override]
        context = super().get_context_data(**kwargs)

        cache_key = "home:upcoming_events:v1"
        upcoming_events: Any = cache.get(cache_key)
        if upcoming_events is None:
            event_manager = cast(Manager, getattr(Event, "objects"))
            upcoming_events = list(
                event_manager.filter(start_time__gte=timezone.now())
                .order_by("start_time")[:3]
                .only("id", "slug", "title", "start_time", "location")
            )
            cache.set(cache_key, upcoming_events, timeout=60)

        context["upcoming_events"] = upcoming_events
        return context


class TermsView(PlainTemplateView):
    template_name = "home/terms.html"


class PrivacyView(PlainTemplateView):
    template_name = "home/privacy.html"


class AboutView(PlainTemplateView):
    template_name = "home/about.html"

    def get_context_data(self, **kwargs):  # type: ignore[override]
        context = super().get_context_data(**kwargs)

        cache_key = "home:upcoming_events:v1"
        upcoming_events: Any = cache.get(cache_key)
        if upcoming_events is None:
            event_manager = cast(Manager, getattr(Event, "objects"))
            upcoming_events = list(
                event_manager.filter(start_time__gte=timezone.now())
                .order_by("start_time")[:3]
                .only("id", "slug", "title", "start_time", "location")
            )
            cache.set(cache_key, upcoming_events, timeout=60)

        context["upcoming_events"] = upcoming_events
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
        event_manager = cast(Manager, getattr(Event, "objects"))
        event_count = event_manager.count()

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
