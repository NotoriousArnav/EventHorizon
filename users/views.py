from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from .models import Profile, SocialLink
from .forms import UserUpdateForm, ProfileUpdateForm, SocialLinkFormSet


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
