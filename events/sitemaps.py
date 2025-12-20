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
