from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, SocialLink


class SocialLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialLink
        fields = ["platform", "url"]


class ProfileSerializer(serializers.ModelSerializer):
    social_links = SocialLinkSerializer(
        source="user.social_links", many=True, read_only=True
    )

    class Meta:
        model = Profile
        fields = ["bio", "location", "phone_number", "avatar", "social_links"]


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "date_joined",
            "profile",
        ]
