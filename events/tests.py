from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from .models import Event, Registration

User = get_user_model()


class EventAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.client.force_authenticate(user=self.user)

        self.event_data = {
            "title": "Test Event",
            "description": "This is a test event.",
            "start_time": timezone.now() + timedelta(days=1),
            "end_time": timezone.now() + timedelta(days=1, hours=2),
            "location": "Test Location",
            "capacity": 10,
        }
        self.event = Event.objects.create(organizer=self.user, **self.event_data)

    def test_create_event(self):
        response = self.client.post("/api/events/", self.event_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Event.objects.count(), 2)

    def test_get_events(self):
        response = self.client.get("/api/events/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Assuming pagination might be involved or structure of response
        # DRF ListCreateAPIView usually returns a list or a paginated dict
        # Since no pagination class is set in settings yet, it should be a list
        self.assertEqual(len(response.data), 1)

    def test_register_event(self):
        new_user = User.objects.create_user(username="participant", password="password")
        self.client.force_authenticate(user=new_user)
        response = self.client.post(f"/api/events/{self.event.id}/register/")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            Registration.objects.filter(event=self.event, participant=new_user).exists()
        )

    def test_duplicate_registration(self):
        new_user = User.objects.create_user(
            username="participant2", password="password"
        )
        self.client.force_authenticate(user=new_user)
        # First registration
        self.client.post(f"/api/events/{self.event.id}/register/")
        # Second registration attempt
        response = self.client.post(f"/api/events/{self.event.id}/register/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_capacity_limit(self):
        small_event = Event.objects.create(
            organizer=self.user,
            title="Small Event",
            description="Small",
            start_time=timezone.now(),
            end_time=timezone.now(),
            location="Room",
            capacity=1,
        )
        # Fill capacity
        user1 = User.objects.create_user(username="u1", password="p")
        Registration.objects.create(event=small_event, participant=user1)

        # Try to register another user
        user2 = User.objects.create_user(username="u2", password="p")
        self.client.force_authenticate(user=user2)
        response = self.client.post(f"/api/events/{small_event.id}/register/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
