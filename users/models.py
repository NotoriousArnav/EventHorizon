from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} Profile"


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
