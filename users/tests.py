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
