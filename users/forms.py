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

from django import forms
from django.contrib.auth.models import User
from .models import Profile, SocialLink
from django.forms import inlineformset_factory


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "appearance-none relative block w-full px-3 py-3 border border-white/10 placeholder-gray-500 text-gray-300 rounded-md focus:outline-none focus:ring-orange-500 focus:border-orange-500 focus:z-10 sm:text-sm bg-black/50 backdrop-blur-sm transition-all duration-300"
            }
        )
    )
    first_name = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "appearance-none relative block w-full px-3 py-3 border border-white/10 placeholder-gray-500 text-gray-300 rounded-md focus:outline-none focus:ring-orange-500 focus:border-orange-500 focus:z-10 sm:text-sm bg-black/50 backdrop-blur-sm transition-all duration-300"
            }
        ),
    )
    last_name = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "appearance-none relative block w-full px-3 py-3 border border-white/10 placeholder-gray-500 text-gray-300 rounded-md focus:outline-none focus:ring-orange-500 focus:border-orange-500 focus:z-10 sm:text-sm bg-black/50 backdrop-blur-sm transition-all duration-300"
            }
        ),
    )

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]


class ProfileUpdateForm(forms.ModelForm):
    bio = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "appearance-none relative block w-full px-3 py-3 border border-white/10 placeholder-gray-500 text-gray-300 rounded-md focus:outline-none focus:ring-orange-500 focus:border-orange-500 focus:z-10 sm:text-sm bg-black/50 backdrop-blur-sm transition-all duration-300",
                "rows": 3,
            }
        ),
        required=False,
    )
    location = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "appearance-none relative block w-full px-3 py-3 border border-white/10 placeholder-gray-500 text-gray-300 rounded-md focus:outline-none focus:ring-orange-500 focus:border-orange-500 focus:z-10 sm:text-sm bg-black/50 backdrop-blur-sm transition-all duration-300"
            }
        ),
    )
    phone_number = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "appearance-none relative block w-full px-3 py-3 border border-white/10 placeholder-gray-500 text-gray-300 rounded-md focus:outline-none focus:ring-orange-500 focus:border-orange-500 focus:z-10 sm:text-sm bg-black/50 backdrop-blur-sm transition-all duration-300"
            }
        ),
    )
    avatar = forms.ImageField(
        required=False,
        widget=forms.FileInput(
            attrs={
                "class": "block w-full text-sm text-gray-300 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-orange-600 file:text-white hover:file:bg-orange-700 file:cursor-pointer cursor-pointer",
                "accept": "image/*",
            }
        ),
        help_text="Upload your profile picture. Large images will be automatically optimized (max 2048x2048px, 5MB).",
    )

    class Meta:
        model = Profile
        fields = ["avatar", "bio", "location", "phone_number"]


class SocialLinkForm(forms.ModelForm):
    platform = forms.ChoiceField(
        required=False,
        choices=SocialLink.PLATFORM_CHOICES,
        widget=forms.Select(
            attrs={
                "class": "appearance-none relative block w-full px-3 py-3 border border-white/10 placeholder-gray-500 text-gray-300 rounded-md focus:outline-none focus:ring-orange-500 focus:border-orange-500 focus:z-10 sm:text-sm bg-black/50 backdrop-blur-sm transition-all duration-300"
            }
        ),
    )
    url = forms.URLField(
        required=False,
        widget=forms.URLInput(
            attrs={
                "class": "appearance-none relative block w-full px-3 py-3 border border-white/10 placeholder-gray-500 text-gray-300 rounded-md focus:outline-none focus:ring-orange-500 focus:border-orange-500 focus:z-10 sm:text-sm bg-black/50 backdrop-blur-sm transition-all duration-300"
            }
        ),
    )

    class Meta:
        model = SocialLink
        fields = ["platform", "url"]

    def clean(self):
        """Ensure that if either field is filled, both must be filled."""
        cleaned_data = super().clean()
        platform = cleaned_data.get("platform")
        url = cleaned_data.get("url")

        # Skip validation for completely empty forms (no URL means it's empty)
        if not url:
            # Clear any errors and don't save this form
            return cleaned_data

        # If URL is provided, platform must be provided too
        if url and not platform:
            raise forms.ValidationError("Please select a platform for the entered URL.")

        return cleaned_data


class BaseSocialLinkFormSet(forms.BaseInlineFormSet):
    """Custom formset that doesn't save empty forms."""

    def save(self, commit=True):
        """Override save to skip empty forms."""
        instances = super().save(commit=False)

        # Filter out instances without URLs (empty forms)
        instances_to_save = [inst for inst in instances if inst.url]

        if commit:
            for instance in instances_to_save:
                instance.save()

        # Handle deletions
        if hasattr(self, "deleted_objects"):
            for obj in self.deleted_objects:  # type: ignore
                obj.delete()

        return instances_to_save


SocialLinkFormSet = inlineformset_factory(
    User,
    SocialLink,
    form=SocialLinkForm,
    formset=BaseSocialLinkFormSet,
    extra=0,  # Don't show empty form by default
    can_delete=True,
    validate_min=False,
    validate_max=False,
)
