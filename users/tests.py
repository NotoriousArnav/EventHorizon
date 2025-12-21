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

from django.contrib.auth import get_user_model
from django.test import TestCase

from .models import Profile, SocialLink


class ProfileSignalTests(TestCase):
    def test_profile_created_on_user_creation(self):
        User = get_user_model()
        user = User.objects.create_user(username="alice", password="password123")

        self.assertTrue(Profile.objects.filter(user=user).exists())

    def test_profile_auto_created_for_existing_user(self):
        User = get_user_model()
        user = User.objects.create_user(username="bob", password="password123")
        Profile.objects.filter(user=user).delete()

        user.first_name = "Bobby"
        user.save()

        self.assertTrue(Profile.objects.filter(user=user).exists())

    def test_social_link_str(self):
        User = get_user_model()
        user = User.objects.create_user(username="charlie", password="password123")
        link = SocialLink.objects.create(
            user=user, platform="github", url="https://github.com/charlie"
        )

        self.assertEqual(str(link), "github - charlie")
