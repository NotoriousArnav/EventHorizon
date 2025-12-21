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

from django import template
from allauth.socialaccount.models import SocialApp

register = template.Library()


@register.simple_tag(takes_context=True)
def get_configured_providers(context):
    """
    Returns a list of provider IDs (e.g., ['google', 'github'])
    that have a SocialApp configured in the database for the current site.
    """
    request = context.get("request")
    if not request:
        return []

    try:
        # Get the current site from the request
        # Note: In a real multi-site setup with django.contrib.sites,
        # we would use Site.objects.get_current(request)
        # But querying SocialApp directly filtering by sites is safer if sites framework is active.

        # This returns SocialApp objects that are attached to the current site
        # We need distinct provider IDs
        from django.contrib.sites.shortcuts import get_current_site

        current_site = get_current_site(request)

        providers = (
            SocialApp.objects.filter(sites=current_site)
            .values_list("provider", flat=True)
            .distinct()
        )
        return list(providers)
    except Exception:
        return []


@register.filter
def provider_name(provider_id):
    """
    Maps provider IDs to display names.
    """
    names = {
        "github": "GitHub",
        "google": "Google",
        "facebook": "Facebook",
        "twitter": "Twitter",
        # Add more mappings as needed
    }
    return names.get(provider_id, provider_id.title())


@register.filter
def provider_class(provider_id):
    """
    Maps provider IDs to specific Tailwind color classes.
    """
    classes = {
        "github": "hover:bg-[#24292F] focus-visible:outline-[#24292F]",
        "google": "hover:bg-white/10 focus-visible:outline-[#1D9BF0]",  # Google doesn't have a solid single bg color usually, using neutral
        "facebook": "hover:bg-[#1877F2] focus-visible:outline-[#1877F2]",
        "twitter": "hover:bg-[#1DA1F2] focus-visible:outline-[#1DA1F2]",
    }
    return classes.get(
        provider_id, "hover:bg-indigo-500 focus-visible:outline-indigo-500"
    )


@register.filter
def provider_icon(provider_id):
    """
    Returns the SVG path for the provider icon.
    """
    icons = {
        "github": "M10 0C4.477 0 0 4.484 0 10.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0110 4.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0020 10.017C20 4.484 15.522 0 10 0z",
        "google": "M12.48 10.92v3.28h7.84c-.24 1.84-.853 3.187-1.787 4.133-1.147 1.147-2.933 2.4-6.053 2.4-4.827 0-8.6-3.893-8.6-8.72s3.773-8.72 8.6-8.72c2.6 0 4.507 1.027 5.907 2.347l2.307-2.307C18.747 1.44 16.133 0 12.48 0 5.867 0 .307 5.387.307 12s5.56 12 12.173 12c3.573 0 6.267-1.173 8.373-3.36 2.16-2.16 2.84-5.213 2.84-7.667 0-.76-.053-1.467-.173-2.053H12.48z",
    }
    return icons.get(provider_id, "")
