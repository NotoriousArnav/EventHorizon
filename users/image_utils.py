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
Image compression utilities for EventHorizon.

Handles automatic image compression for user-uploaded avatars
to reduce storage costs while maintaining acceptable quality.
"""

from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys


def compress_image(image_file, max_size_mb=5, quality=85, max_dimension=2048):
    """
    Compress an image to ensure it's under the specified size limit.

    Args:
        image_file: The uploaded image file
        max_size_mb: Maximum file size in megabytes (default: 5MB)
        quality: JPEG quality (1-100, default: 85)
        max_dimension: Maximum width/height in pixels (default: 2048)

    Returns:
        Compressed image file or original if already small enough
    """
    # Open the image
    img = Image.open(image_file)

    # Convert RGBA to RGB if necessary (for JPEG compatibility)
    if img.mode in ("RGBA", "LA", "P"):
        # Create a white background
        background = Image.new("RGB", img.size, (255, 255, 255))
        if img.mode == "P":
            img = img.convert("RGBA")
        background.paste(
            img, mask=img.split()[-1] if img.mode in ("RGBA", "LA") else None
        )
        img = background
    elif img.mode != "RGB":
        img = img.convert("RGB")

    # Resize if image is too large
    if img.width > max_dimension or img.height > max_dimension:
        img.thumbnail((max_dimension, max_dimension), Image.Resampling.LANCZOS)

    # Compress the image iteratively until it's under max_size_mb
    max_size_bytes = max_size_mb * 1024 * 1024
    output = BytesIO()
    current_quality = quality

    # First attempt with specified quality
    img.save(output, format="JPEG", quality=current_quality, optimize=True)

    # If still too large, reduce quality iteratively
    while output.tell() > max_size_bytes and current_quality > 20:
        output = BytesIO()
        current_quality -= 5
        img.save(output, format="JPEG", quality=current_quality, optimize=True)

    # Get the file size for logging
    output.seek(0, 2)  # Seek to end
    file_size = output.tell()
    output.seek(0)  # Reset to beginning

    # Create a new InMemoryUploadedFile
    compressed_file = InMemoryUploadedFile(
        output,
        "ImageField",
        f"{image_file.name.split('.')[0]}.jpg",  # Force .jpg extension
        "image/jpeg",
        sys.getsizeof(output),
        None,
    )

    return compressed_file, file_size


def format_bytes(bytes_size):
    """
    Format bytes to human-readable size.

    Args:
        bytes_size: Size in bytes

    Returns:
        Formatted string (e.g., "2.5 MB")
    """
    for unit in ["B", "KB", "MB", "GB"]:
        if bytes_size < 1024.0:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.2f} TB"
