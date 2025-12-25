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

from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core import mail
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIClient

from .models import Event, Registration

User = get_user_model()


@override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
class EventTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.api_client = APIClient()

        self.user = User.objects.create_user(
            username="testuser", password="password", email="testuser@example.com"
        )
        self.organizer = User.objects.create_user(
            username="organizer", password="password", email="organizer@example.com"
        )

        self.client.login(username="testuser", password="password")
        self.api_client.force_authenticate(user=self.user)

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
        self.assertEqual(response.status_code, 302)

        created_event = Event.objects.get(title="Test Event")
        self.assertEqual(created_event.organizer, self.organizer)
        self.assertTrue(created_event.slug)

    def test_list_events(self):
        Event.objects.create(organizer=self.organizer, **self.event_data)
        response = self.client.get(reverse("event-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Event")

    def test_register_event_sends_organizer_and_participant_emails(self):
        event = Event.objects.create(organizer=self.organizer, **self.event_data)
        response = self.client.post(
            reverse("event-register", kwargs={"slug": event.slug})
        )
        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            Registration.objects.filter(event=event, participant=self.user).exists()
        )

        self.assertEqual(len(mail.outbox), 2)
        emails_by_recipient = {msg.to[0]: msg for msg in mail.outbox}

        self.assertIn("organizer@example.com", emails_by_recipient)
        organizer_email = emails_by_recipient["organizer@example.com"]
        self.assertGreater(len(organizer_email.alternatives), 0)
        self.assertEqual(organizer_email.alternatives[0][1], "text/html")

        self.assertIn("testuser@example.com", emails_by_recipient)
        participant_email = emails_by_recipient["testuser@example.com"]
        self.assertGreater(len(participant_email.alternatives), 0)
        self.assertEqual(participant_email.alternatives[0][1], "text/html")
        self.assertIn("Your registration has been recorded", participant_email.body)

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

        Registration.objects.create(
            event=small_event, participant=self.organizer, status="registered"
        )

        response = self.client.post(
            reverse("event-register", kwargs={"slug": small_event.slug})
        )
        self.assertEqual(response.status_code, 302)

        registration = Registration.objects.get(
            event=small_event, participant=self.user
        )
        self.assertEqual(registration.status, "waitlisted")

    def test_manage_registration_sends_status_changed_email(self):
        event = Event.objects.create(organizer=self.organizer, **self.event_data)
        registration = Registration.objects.create(
            event=event, participant=self.user, status="waitlisted"
        )

        self.client.logout()
        self.client.login(username="organizer", password="password")

        response = self.client.post(
            reverse("manage-registration", kwargs={"registration_id": registration.id}),
            {"action": "approve"},
        )
        self.assertEqual(response.status_code, 302)

        registration.refresh_from_db()
        self.assertEqual(registration.status, "registered")

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ["testuser@example.com"])
        self.assertIn("Your registration has been recorded", mail.outbox[0].body)

    def test_api_register_waitlists_when_full(self):
        event = Event.objects.create(organizer=self.organizer, **self.event_data)
        Registration.objects.create(
            event=event, participant=self.organizer, status="registered"
        )
        event.capacity = 1
        event.save(update_fields=["capacity"])

        response = self.api_client.post(
            reverse("api-events-register", kwargs={"pk": event.pk}),
            data={"answers": {}},
            format="json",
        )
        self.assertEqual(response.status_code, 201)

        registration = Registration.objects.get(event=event, participant=self.user)
        self.assertEqual(registration.status, "waitlisted")
