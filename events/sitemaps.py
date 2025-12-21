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

"""
Sitemap configuration for Event Horizon
Defines XML sitemaps for search engine indexing
"""

from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from events.models import Event
from django.contrib.auth.models import User


class StaticViewSitemap(Sitemap):
    """Sitemap for static pages"""

    priority = 0.8
    changefreq = "weekly"

    def items(self):
        return ["home", "event-list"]

    def location(self, item):
        return reverse(item)


class EventSitemap(Sitemap):
    """Sitemap for event pages"""

    changefreq = "daily"
    priority = 0.9

    def items(self):
        # Only include upcoming events in sitemap
        from django.utils import timezone

        return Event.objects.filter(start_time__gte=timezone.now()).order_by(
            "-created_at"
        )

    def lastmod(self, item):
        return item.updated_at

    def location(self, item):
        return reverse("event-detail", args=[item.slug])
