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

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .image_utils import compress_image, format_bytes
import logging

logger = logging.getLogger(__name__)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} Profile"

    def save(self, *args, **kwargs):
        """Override save to compress avatar image before saving."""
        if self.avatar and hasattr(self.avatar, "file"):
            try:
                # Get original file size
                original_size = self.avatar.size

                # Compress the image (max 5MB, quality 85)
                compressed_file, compressed_size = compress_image(
                    self.avatar.file, max_size_mb=5, quality=85, max_dimension=2048
                )

                # Replace the avatar with compressed version
                self.avatar = compressed_file

                # Log compression stats
                logger.info(
                    f"Avatar compressed for user {self.user.username}: "
                    f"{format_bytes(original_size)} -> {format_bytes(compressed_size)} "
                    f"({(1 - compressed_size / original_size) * 100:.1f}% reduction)"
                )
            except Exception as e:
                # If compression fails, log error but continue with original image
                logger.error(
                    f"Failed to compress avatar for user {self.user.username}: {str(e)}"
                )

        super().save(*args, **kwargs)


class SocialLink(models.Model):
    PLATFORM_CHOICES = [
        ("github", "GitHub"),
        ("twitter", "Twitter/X"),
        ("linkedin", "LinkedIn"),
        ("instagram", "Instagram"),
        ("facebook", "Facebook"),
        ("website", "Personal Website"),
        ("other", "Other"),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="social_links"
    )
    platform = models.CharField(
        max_length=20, choices=PLATFORM_CHOICES, default="other"
    )
    url = models.URLField()

    def __str__(self):
        return f"{self.platform} - {self.user.username}"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    # This prevents the RelatedObjectDoesNotExist error
    # If the user already exists but has no profile (e.g., superuser created before this app),
    # accessing instance.profile would crash.
    # We should only save if it exists, or create it if missing (though the create signal usually handles that for new users).

    # Check if profile exists safely
    if hasattr(instance, "profile"):
        instance.profile.save()
    else:
        # For legacy users (like your superuser) that don't have a profile yet
        Profile.objects.create(user=instance)
