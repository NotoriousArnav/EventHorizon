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
                "class": "appearance-none relative block w-full px-3 py-3 border border-white/10 placeholder-gray-500 text-gray-300 rounded-md focus:outline-none focus:ring-orange-500 focus:border-orange-500 focus:z-10 sm:text-sm bg-black/50 backdrop-blur-sm transition-all duration-300"
            }
        ),
    )

    class Meta:
        model = Profile
        fields = ["avatar", "bio", "location", "phone_number"]


class SocialLinkForm(forms.ModelForm):
    platform = forms.ChoiceField(
        choices=SocialLink.PLATFORM_CHOICES,
        widget=forms.Select(
            attrs={
                "class": "appearance-none relative block w-full px-3 py-3 border border-white/10 placeholder-gray-500 text-gray-300 rounded-md focus:outline-none focus:ring-orange-500 focus:border-orange-500 focus:z-10 sm:text-sm bg-black/50 backdrop-blur-sm transition-all duration-300"
            }
        ),
    )
    url = forms.URLField(
        widget=forms.URLInput(
            attrs={
                "class": "appearance-none relative block w-full px-3 py-3 border border-white/10 placeholder-gray-500 text-gray-300 rounded-md focus:outline-none focus:ring-orange-500 focus:border-orange-500 focus:z-10 sm:text-sm bg-black/50 backdrop-blur-sm transition-all duration-300"
            }
        )
    )

    class Meta:
        model = SocialLink
        fields = ["platform", "url"]


SocialLinkFormSet = inlineformset_factory(
    User, SocialLink, form=SocialLinkForm, extra=1, can_delete=True
)
