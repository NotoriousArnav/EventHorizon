# SEO Implementation Guide

## Overview

Event Horizon has been enhanced with comprehensive SEO (Search Engine Optimization) features to improve search engine visibility, social media sharing, and overall discoverability.

## Features Implemented

### 1. Meta Tags

All pages now include:

- **Primary Meta Tags**: Title, description, keywords, author, and robots directives
- **Open Graph Tags**: Optimized for Facebook, LinkedIn, and other social platforms
- **Twitter Card Tags**: Enhanced Twitter sharing with rich previews
- **Canonical URLs**: Prevent duplicate content issues

#### Template Structure

The base template (`base.html`) provides default meta tags that can be overridden in child templates:

{% raw %}
```django
{% block title %}Page Title{% endblock %}
{% block meta_description %}Page description{% endblock %}
{% block og_title %}Social media title{% endblock %}
```
{% endraw %}

### 2. Structured Data (JSON-LD)

Implemented Schema.org structured data for:

- **Events**: Full event information including organizer, location, dates, and availability
- **User Profiles**: Person schema for public profiles
- **Website**: SearchAction schema for site-wide search functionality

Example event structured data:
```json
{
  "@context": "https://schema.org",
  "@type": "Event",
  "name": "Event Title",
  "startDate": "2025-01-01T10:00:00Z",
  "location": {...},
  "organizer": {...}
}
```

### 3. Sitemaps

Dynamic XML sitemaps are generated at `/sitemap.xml`:

- **Static Pages**: Home and event list pages
- **Events**: All upcoming events (updated daily)
- Priority and change frequency configured per section

Location: `events/sitemaps.py`

### 4. Robots.txt

Search engine crawling instructions at `/robots.txt`:

- Allows crawling of public pages
- Blocks admin, authentication, and private areas
- References sitemap location
- Protects user-uploaded content (avatars)

Location: `templates/robots.txt`

### 5. Image Accessibility

All images now include descriptive `alt` attributes:

- User avatars: "Username's profile avatar"
- Event organizer photos: "Organizer name avatar"
- Decorative elements: `aria-hidden="true"` or `aria-label`

### 6. Semantic HTML

Improved heading hierarchy:

- Single `<h1>` per page (main title)
- Proper `<h2>`, `<h3>` nesting for content sections
- ARIA labels for screen readers on decorative elements

## Configuration

### Settings (settings.py)

1. Added `django.contrib.sitemaps` to `INSTALLED_APPS`
2. Added `EventHorizon.context_processors.seo_context` to context processors

### URLs (EventHorizon/urls.py)

```python
from events.sitemaps import StaticViewSitemap, EventSitemap

sitemaps = {
    'static': StaticViewSitemap,
    'events': EventSitemap,
}

urlpatterns = [
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    # ... other urls
]
```

## Usage Guidelines

### Adding SEO to New Pages

1. **Extend the base template** and override SEO blocks:

{% raw %}
```django
{% extends "base.html" %}

{% block title %}My Page Title{% endblock %}
{% block meta_description %}A compelling description under 160 characters{% endblock %}
{% block meta_keywords %}keyword1, keyword2, keyword3{% endblock %}

{% block og_title %}Social Media Title{% endblock %}
{% block og_description %}Description for social media sharing{% endblock %}

{% block structured_data %}
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Thing",
  "name": "Your structured data"
}
</script>
{% endblock %}
```
{% endraw %}

2. **Ensure images have alt text**:

```html
<img src="..." alt="Descriptive text">
```

3. **Use semantic heading hierarchy**:

```html
<h1>Main Page Title</h1>
<section>
  <h2>Section Title</h2>
  <h3>Subsection</h3>
</section>
```

### Best Practices

1. **Title Tags**: 50-60 characters, include keywords, make it unique per page
2. **Meta Descriptions**: 150-160 characters, compelling call-to-action
3. **Keywords**: 5-10 relevant keywords, comma-separated
4. **Canonical URLs**: Set for pages with multiple URLs
5. **Structured Data**: Validate using Google's Rich Results Test
6. **Images**: Always include alt text, optimize file sizes
7. **Robots Meta**: Use `noindex, nofollow` for private/duplicate pages

## Testing & Validation

### Tools

1. **Google Search Console**: Submit sitemap, monitor indexing
2. **Schema Markup Validator**: https://validator.schema.org/
3. **Facebook Sharing Debugger**: https://developers.facebook.com/tools/debug/
4. **Twitter Card Validator**: https://cards-dev.twitter.com/validator
5. **Google Rich Results Test**: https://search.google.com/test/rich-results

### Manual Checks

```bash
# Test sitemap
curl http://localhost:8000/sitemap.xml

# Test robots.txt
curl http://localhost:8000/robots.txt

# Validate HTML
https://validator.w3.org/
```

## Sitemap Management

The sitemap automatically includes:

- **Upcoming events only**: Past events are excluded
- **Last modified dates**: Based on `updated_at` field
- **Priority scores**: Events (0.9), Static pages (0.8)

To manually update sitemap configuration, edit `events/sitemaps.py`.

## Robots.txt Customization

To modify crawling rules:

1. Edit `templates/robots.txt`
2. Add/remove Disallow rules
3. Restart the server

Example - Block a specific section:
```
User-agent: *
Disallow: /private-section/
```

## Social Media Optimization

### Facebook/LinkedIn

Uses Open Graph protocol. Preview how posts will appear:
- Facebook: https://developers.facebook.com/tools/debug/
- LinkedIn: https://www.linkedin.com/post-inspector/

### Twitter

Uses Twitter Card markup. Card types available:
- `summary`: Default card with thumbnail
- `summary_large_image`: Large image card (current default)

## Future Enhancements

Recommended improvements:

1. **Image Optimization**
   - Add default OG/Twitter images to static files
   - Implement dynamic image generation for event cards
   - Use CDN for faster image delivery

2. **Advanced Structured Data**
   - BreadcrumbList for navigation
   - Organization schema
   - FAQ schema for help pages
   - Review/Rating schema for events

3. **Performance**
   - Add meta tags for preconnect/prefetch
   - Implement lazy loading for images
   - Add resource hints

4. **Analytics Integration**
   - Google Analytics 4
   - Google Tag Manager
   - Event tracking for registrations

5. **Multi-language Support**
   - hreflang tags for internationalization
   - Language-specific sitemaps

6. **Rich Snippets**
   - Event countdown timers
   - Star ratings for events
   - Organizer badges

## Monitoring

### Key Metrics to Track

1. **Search Console**
   - Impressions and clicks
   - Average position
   - CTR (Click-through rate)
   - Coverage issues

2. **Page Speed**
   - Core Web Vitals (LCP, FID, CLS)
   - Mobile performance
   - Time to Interactive

3. **Social Sharing**
   - Share counts
   - Engagement rates
   - Referral traffic

## Support

For issues or questions:
- Review Django Sitemaps docs: https://docs.djangoproject.com/en/stable/ref/contrib/sitemaps/
- Schema.org documentation: https://schema.org/
- Open Graph protocol: https://ogp.me/

## Changelog

### 2025-12-20 - Initial Implementation

- Added comprehensive meta tags to base.html
- Implemented Open Graph and Twitter Card support
- Created dynamic sitemap for events and static pages
- Added robots.txt with crawler directives
- Implemented JSON-LD structured data for events and profiles
- Enhanced image accessibility with alt attributes
- Improved semantic HTML structure
- Added SEO context processor
- Updated documentation
