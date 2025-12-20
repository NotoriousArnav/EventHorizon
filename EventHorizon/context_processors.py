"""
Context processors for Event Horizon
Provides additional context variables to all templates
"""

from django.conf import settings


def seo_context(request):
    """
    Adds SEO-related context variables to all templates
    """
    return {
        "sitemap_url": request.build_absolute_uri("/sitemap.xml"),
        "site_name": "Event Horizon",
        "site_url": f"{request.scheme}://{request.get_host()}",
    }
