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
