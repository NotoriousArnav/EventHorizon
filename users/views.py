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

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from .models import Profile, SocialLink
from .forms import UserUpdateForm, ProfileUpdateForm, SocialLinkFormSet
from oauth2_provider.models import Application
from knox.models import AuthToken
from django.utils import timezone


@login_required
def profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile
        )

        # Handle Social Links
        s_formset = SocialLinkFormSet(request.POST, instance=request.user)

        if u_form.is_valid() and p_form.is_valid() and s_formset.is_valid():
            # Check if a new avatar was uploaded
            if "avatar" in request.FILES:
                avatar_file = request.FILES["avatar"]
                original_size = avatar_file.size

                # Info message about image compression
                if original_size > 5 * 1024 * 1024:  # > 5MB
                    messages.info(
                        request,
                        _(
                            "Large image detected. Your image will be automatically compressed to ensure fast loading times."
                        ),
                    )
                elif original_size > 1 * 1024 * 1024:  # > 1MB
                    messages.info(
                        request,
                        _(
                            "Your image will be optimized for web viewing to ensure the best performance."
                        ),
                    )

            u_form.save()
            p_form.save()
            s_formset.save()
            messages.success(request, _("Your profile has been updated!"))
            return redirect("profile")
        else:
            # Show error message if validation fails
            messages.error(request, _("Please correct the errors below."))
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        s_formset = SocialLinkFormSet(instance=request.user)

    context = {
        "u_form": u_form,
        "p_form": p_form,
        "s_formset": s_formset,
        "title": f"Profile | {request.user.username}",
    }

    return render(request, "users/profile.html", context)


@login_required
def oauth2_apps(request):
    """Manage OAuth2 applications"""
    apps = Application.objects.filter(user=request.user).order_by("-created")

    # Get new app credentials from session if they exist
    new_oauth_app_name = request.session.get("new_oauth_app_name")
    new_oauth_client_id = request.session.get("new_oauth_client_id")
    new_oauth_client_secret = request.session.get("new_oauth_client_secret")

    context = {
        "apps": apps,
        "title": "OAuth2 Applications",
        "new_oauth_app_name": new_oauth_app_name,
        "new_oauth_client_id": new_oauth_client_id,
        "new_oauth_client_secret": new_oauth_client_secret,
    }

    # Clear the session variables after rendering
    if "new_oauth_app_id" in request.session:
        del request.session["new_oauth_app_id"]
    if "new_oauth_app_name" in request.session:
        del request.session["new_oauth_app_name"]
    if "new_oauth_client_id" in request.session:
        del request.session["new_oauth_client_id"]
    if "new_oauth_client_secret" in request.session:
        del request.session["new_oauth_client_secret"]

    return render(request, "users/oauth2_apps.html", context)


@login_required
def oauth2_app_create(request):
    """Create a new OAuth2 application"""
    if request.method == "POST":
        name = request.POST.get("name")
        client_type = request.POST.get("client_type", Application.CLIENT_CONFIDENTIAL)
        authorization_grant_type = request.POST.get(
            "authorization_grant_type", Application.GRANT_AUTHORIZATION_CODE
        )
        redirect_uris = request.POST.get("redirect_uris", "")

        if name:
            app = Application.objects.create(
                user=request.user,
                name=name,
                client_type=client_type,
                authorization_grant_type=authorization_grant_type,
                redirect_uris=redirect_uris,
            )

            # Store credentials in session to show once
            request.session["new_oauth_app_id"] = str(app.id)
            request.session["new_oauth_app_name"] = app.name
            request.session["new_oauth_client_id"] = app.client_id
            request.session["new_oauth_client_secret"] = app.client_secret

            messages.success(
                request,
                f"OAuth2 application '{name}' created successfully! Make sure to copy your Client Secret now.",
            )
            return redirect("oauth2-apps")
        else:
            messages.error(request, "Application name is required.")

    context = {
        "title": "Create OAuth2 Application",
        "client_types": Application.CLIENT_TYPES,
        "grant_types": Application.GRANT_TYPES,
    }

    return render(request, "users/oauth2_app_form.html", context)


@login_required
def oauth2_app_delete(request, app_id):
    """Delete an OAuth2 application"""
    app = get_object_or_404(Application, id=app_id, user=request.user)

    if request.method == "POST":
        app_name = app.name
        app.delete()
        messages.success(
            request, f"OAuth2 application '{app_name}' deleted successfully!"
        )
        return redirect("oauth2-apps")

    context = {
        "app": app,
        "title": f"Delete {app.name}",
    }

    return render(request, "users/oauth2_app_confirm_delete.html", context)


@login_required
def api_keys(request):
    """Manage API Keys (Knox tokens)"""
    tokens = AuthToken.objects.filter(user=request.user).order_by("-created")

    # Get the new API key from session if it exists
    new_api_key = request.session.get("new_api_key")

    context = {
        "tokens": tokens,
        "title": "API Keys",
        "new_api_key": new_api_key,
    }

    # Clear the session variable after rendering
    if "new_api_key" in request.session:
        del request.session["new_api_key"]
    if "new_api_key_name" in request.session:
        del request.session["new_api_key_name"]

    return render(request, "users/api_keys.html", context)


@login_required
def api_key_create(request):
    """Create a new API key"""
    if request.method == "POST":
        name = request.POST.get(
            "name", f"API Key {timezone.now().strftime('%Y-%m-%d %H:%M')}"
        )

        # Create Knox token
        instance, token = AuthToken.objects.create(user=request.user)

        # Store the token in session to display once
        request.session["new_api_key"] = token
        request.session["new_api_key_name"] = name

        messages.success(
            request,
            "API Key created successfully! Make sure to copy it now - you won't be able to see it again.",
        )
        return redirect("api-keys")

    context = {
        "title": "Create API Key",
    }

    return render(request, "users/api_key_form.html", context)


@login_required
def api_key_delete(request, token_id):
    """Delete an API key"""
    token = get_object_or_404(AuthToken, digest=token_id, user=request.user)

    if request.method == "POST":
        token.delete()
        messages.success(request, "API Key deleted successfully!")
        return redirect("api-keys")

    context = {
        "token": token,
        "title": "Delete API Key",
    }

    return render(request, "users/api_key_confirm_delete.html", context)
