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

"""
Custom Allauth Account Adapter for Event Horizon

Provides special handling for staff and superuser accounts:
- Auto-verifies staff/superuser email addresses
- Allows staff/superusers to login without email verification
"""

from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.models import EmailAddress


class CustomAccountAdapter(DefaultAccountAdapter):
    """
    Custom account adapter that provides special handling for staff and superuser accounts.

    Features:
    - Staff and superusers get auto-verified emails
    - Staff and superusers can login without email verification
    - Regular users follow normal verification flow
    """

    def save_user(self, request, user, form, commit=True):
        """
        Save user and auto-verify email for staff/superuser accounts.
        """
        user = super().save_user(request, user, form, commit=False)

        if commit:
            user.save()

            # Auto-verify staff and superuser emails
            if user.is_staff or user.is_superuser:
                email_address, created = EmailAddress.objects.get_or_create(
                    user=user,
                    email=user.email.lower(),
                    defaults={"verified": True, "primary": True},
                )

                if not created and not email_address.verified:
                    # Update existing unverified email
                    email_address.verified = True
                    email_address.primary = True
                    email_address.save()

        return user

    def login(self, request, user):
        """
        Override login to allow staff/superusers even if email is not verified.

        This is called during the login process. If the user is staff or superuser,
        we ensure their email is verified before the check happens.
        """
        # Auto-verify staff/superuser emails on login attempt
        if user.is_staff or user.is_superuser:
            # Make sure email address exists and is verified
            if user.email:
                email_address, created = EmailAddress.objects.get_or_create(
                    user=user,
                    email=user.email.lower(),
                    defaults={"verified": True, "primary": True},
                )

                if not email_address.verified:
                    email_address.verified = True
                    email_address.primary = True
                    email_address.save()

        return super().login(request, user)
