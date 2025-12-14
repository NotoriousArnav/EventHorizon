from django.db import models
from django.conf import settings
from django.utils.text import slugify


class Event(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    location = models.CharField(max_length=255)
    capacity = models.PositiveIntegerField()
    organizer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="hosted_events"
    )
    # Stores a list of questions: [{"id": "q1", "label": "What is your job title?", "type": "text"}]
    registration_schema = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            # Basic slugify
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            # Ensure uniqueness
            while Event.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.title)


class Registration(models.Model):
    STATUS_CHOICES = [
        ("registered", "Registered"),
        ("waitlisted", "Waitlisted"),
        ("cancelled", "Cancelled"),
    ]

    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name="registrations"
    )
    participant = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="registrations"
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="registered"
    )
    # Stores answers: {"q1": "Software Engineer"}
    answers = models.JSONField(default=dict, blank=True)
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("event", "participant")

    def __str__(self):
        return f"{self.participant} - {self.event.title}"
