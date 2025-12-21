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
S3-compatible storage backend for EventHorizon.

Supports:
- AWS S3
- MinIO
- DigitalOcean Spaces
- Cloudflare R2
- Any S3-compatible storage service

This backend uses django-storages with boto3 for S3 operations.
"""

from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class S3MediaStorage(S3Boto3Storage):
    """
    S3-compatible storage backend for user-uploaded media files.

    Configuration is loaded from Django settings which reads from environment variables.

    Features:
    - Automatic public read access for media files
    - Custom domain support for CDN
    - File overwrite protection
    - Optimized for serving user uploads (avatars, event images, etc.)

    Environment variables (set in .env):
        AWS_ACCESS_KEY_ID: S3 access key
        AWS_SECRET_ACCESS_KEY: S3 secret key
        AWS_STORAGE_BUCKET_NAME: Bucket name
        AWS_S3_REGION_NAME: AWS region (e.g., us-east-1)
        AWS_S3_ENDPOINT_URL: Custom endpoint for MinIO/Spaces (optional)
        AWS_S3_CUSTOM_DOMAIN: CDN domain (optional)
        AWS_S3_USE_SSL: Use SSL for connections (default: True)
    """

    location = "media"  # Store media files in /media prefix
    default_acl = "public-read"  # Make uploaded files publicly accessible
    file_overwrite = False  # Don't overwrite existing files

    @property
    def custom_domain(self):
        """Get custom domain from settings if configured."""
        return getattr(settings, "AWS_S3_CUSTOM_DOMAIN", None)


class S3StaticStorage(S3Boto3Storage):
    """
    S3-compatible storage backend for static files (CSS, JS, images).

    Features:
    - Optimized for static file serving
    - Long cache times
    - File overwriting enabled (for collectstatic)

    Note: In most cases, you'll serve static files directly from your server
    or use a CDN. This class is provided for flexibility.
    """

    location = "static"  # Store static files in /static prefix
    default_acl = "public-read"
    file_overwrite = True  # Allow overwriting during collectstatic

    @property
    def custom_domain(self):
        """Get custom domain from settings if configured."""
        return getattr(settings, "AWS_S3_CUSTOM_DOMAIN", None)


class S3PrivateStorage(S3Boto3Storage):
    """
    S3-compatible storage backend for private files.

    Features:
    - Files are private by default
    - Access via pre-signed URLs with expiration
    - Useful for: invoices, private documents, etc.

    Usage:
        from storage.s3 import S3PrivateStorage

        class Document(models.Model):
            file = models.FileField(storage=S3PrivateStorage())

        # Get a temporary URL (valid for 1 hour by default)
        url = document.file.url
    """

    location = "private"
    default_acl = "private"
    file_overwrite = False
    querystring_auth = True  # Generate signed URLs
    querystring_expire = 3600  # URLs expire after 1 hour
    custom_domain = False  # Don't use CDN for private files
