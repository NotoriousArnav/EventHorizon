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

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from .models import Event, Registration
from .utils import extract_registration_schema

User = get_user_model()


class EventTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="password")
        self.organizer = User.objects.create_user(
            username="organizer", password="password"
        )
        self.client.login(username="testuser", password="password")

        self.event_data = {
            "title": "Test Event",
            "description": "A test event description",
            "start_time": timezone.now() + timedelta(days=1),
            "end_time": timezone.now() + timedelta(days=1, hours=2),
            "location": "Test Location",
            "capacity": 10,
        }

    def test_create_event(self):
        self.client.logout()
        self.client.login(username="organizer", password="password")
        response = self.client.post(reverse("event-create"), self.event_data)
        # Redirects to detail view on success
        self.assertEqual(response.status_code, 302)
        created_event = Event.objects.get(title="Test Event")
        self.assertEqual(created_event.organizer, self.organizer)
        self.assertTrue(created_event.slug)

    def test_list_events(self):
        Event.objects.create(organizer=self.organizer, **self.event_data)
        response = self.client.get(reverse("event-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Event")

    def test_register_event(self):
        event = Event.objects.create(organizer=self.organizer, **self.event_data)
        response = self.client.post(
            reverse("event-register", kwargs={"slug": event.slug})
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Registration.objects.filter(event=event, participant=self.user).exists()
        )

    def test_waitlist_logic(self):
        small_event = Event.objects.create(
            organizer=self.organizer,
            title="Small Event",
            description="Tiny",
            start_time=timezone.now(),
            end_time=timezone.now(),
            location="Room",
            capacity=1,
        )
        # Register user 1 (Success)
        Registration.objects.create(
            event=small_event, participant=self.organizer, status="registered"
        )

        # Register user 2 (Waitlist)
        response = self.client.post(
            reverse("event-register", kwargs={"slug": small_event.slug})
        )
        self.assertEqual(response.status_code, 302)
        registration = Registration.objects.get(
            event=small_event, participant=self.user
        )
        self.assertEqual(registration.status, "waitlisted")
