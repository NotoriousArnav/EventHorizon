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
EventHorizon Storage Module

A flexible, provider-agnostic storage system that supports multiple storage backends:
- Local filesystem (development)
- S3-compatible storage (MinIO, AWS S3, DigitalOcean Spaces, Cloudflare R2)
- Supabase Storage (future)
- Vercel Blob (future)
- And more...

Usage:
    Configure storage backend via environment variables in .env:
    STORAGE_BACKEND=s3  # Options: local, s3, minio (alias for s3)

    The storage backend is automatically selected based on settings.py configuration.
"""

from .factory import get_storage_backend

__all__ = ["get_storage_backend"]
