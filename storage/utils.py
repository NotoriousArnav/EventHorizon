"""
Storage utility functions for EventHorizon.

Helper functions for common storage operations.
"""

import os
from typing import Optional
from uuid import uuid4


def generate_unique_filename(instance, filename: str, prefix: str = "") -> str:
    """
    Generate a unique filename with optional prefix.

    Args:
        instance: Model instance (for upload_to callable)
        filename: Original filename
        prefix: Optional prefix for the filename

    Returns:
        Unique filename path

    Example:
        >>> generate_unique_filename(user, "avatar.jpg", "avatars")
        'avatars/a1b2c3d4-avatar.jpg'
    """
    ext = os.path.splitext(filename)[1].lower()
    unique_name = f"{uuid4().hex[:8]}-{filename}"

    if prefix:
        return os.path.join(prefix, unique_name)
    return unique_name


def generate_avatar_path(instance, filename: str) -> str:
    """
    Generate upload path for user avatars.

    Args:
        instance: User profile instance
        filename: Original filename

    Returns:
        Upload path for the avatar

    Example:
        >>> generate_avatar_path(profile, "photo.jpg")
        'avatars/users/123/a1b2c3d4.jpg'
    """
    ext = os.path.splitext(filename)[1].lower()
    unique_name = f"{uuid4().hex}{ext}"
    return os.path.join("avatars", "users", str(instance.user.id), unique_name)


def get_file_extension(filename: str) -> str:
    """
    Get the file extension from a filename.

    Args:
        filename: The filename

    Returns:
        File extension (including the dot)
    """
    return os.path.splitext(filename)[1].lower()


def validate_image_extension(
    filename: str, allowed_extensions: Optional[list] = None
) -> bool:
    """
    Validate if a file has an allowed image extension.

    Args:
        filename: The filename to validate
        allowed_extensions: List of allowed extensions (default: common image formats)

    Returns:
        True if extension is allowed, False otherwise
    """
    if allowed_extensions is None:
        allowed_extensions = [".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg"]

    ext = get_file_extension(filename)
    return ext in allowed_extensions


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human-readable format.

    Args:
        size_bytes: File size in bytes

    Returns:
        Formatted file size string

    Example:
        >>> format_file_size(1024)
        '1.00 KB'
        >>> format_file_size(1048576)
        '1.00 MB'
    """
    size: float = float(size_bytes)
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0
    return f"{size:.2f} PB"
