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
Storage backend factory for EventHorizon.

This module provides a factory function to get the appropriate storage backend
based on configuration.
"""

from django.conf import settings
from django.core.files.storage import FileSystemStorage


def get_storage_backend(storage_type: str = "media"):
    """
    Get the appropriate storage backend based on settings.

    Args:
        storage_type: Type of storage needed ('media', 'static', or 'private')

    Returns:
        Storage backend instance

    Raises:
        ValueError: If an unknown storage backend is requested
    """
    backend = getattr(settings, "STORAGE_BACKEND", "local").lower()

    if backend == "local":
        # Use Django's default filesystem storage
        return FileSystemStorage()

    elif backend in ["s3", "minio"]:
        # S3-compatible storage (AWS S3, MinIO, DigitalOcean Spaces, etc.)
        from .s3 import S3MediaStorage, S3StaticStorage, S3PrivateStorage

        if storage_type == "media":
            return S3MediaStorage()
        elif storage_type == "static":
            return S3StaticStorage()
        elif storage_type == "private":
            return S3PrivateStorage()
        else:
            raise ValueError(f"Unknown storage type: {storage_type}")

    # Future storage backends will be added here:
    # elif backend == "supabase":
    #     from .supabase import SupabaseStorage
    #     return SupabaseStorage()
    #
    # elif backend == "vercel":
    #     from .vercel import VercelBlobStorage
    #     return VercelBlobStorage()

    else:
        raise ValueError(
            f"Unknown storage backend: {backend}. "
            f"Valid options: local, s3, minio (more coming soon: supabase, vercel)"
        )


def get_media_storage():
    """Convenience function to get media storage backend."""
    return get_storage_backend("media")


def get_static_storage():
    """Convenience function to get static storage backend."""
    return get_storage_backend("static")


def get_private_storage():
    """Convenience function to get private storage backend."""
    return get_storage_backend("private")
