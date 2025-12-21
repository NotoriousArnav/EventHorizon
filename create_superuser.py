#!/usr/bin/env python3
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
Event Horizon - Superuser Creation Module
Provides functions for creating superuser accounts programmatically.
"""

import os
import sys


def setup_django():
    """Initialize Django environment."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "EventHorizon.settings")
    import django

    django.setup()


def create_superuser(
    username="admin",
    email="admin@eventhorizon.local",
    password="Ihapwics123$",
    first_name="Administrator",
    last_name="Staff",
    verbose=True,
):
    """
    Create a superuser account with specified credentials.

    Args:
        username (str): Username for the superuser
        email (str): Email address for the superuser
        password (str): Password for the superuser
        first_name (str): First name of the superuser
        last_name (str): Last name of the superuser
        verbose (bool): Whether to print status messages

    Returns:
        tuple: (success: bool, message: str)
    """
    try:
        from django.contrib.auth import get_user_model

        User = get_user_model()

        if User.objects.filter(username=username).exists():
            message = f"Superuser '{username}' already exists."
            if verbose:
                print(message)
            return False, message

        if verbose:
            print(f"Creating superuser '{username}'...")

        User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )

        message = (
            f"Superuser '{username}' created successfully with password '{password}'"
        )
        if verbose:
            print(message)

        return True, message

    except Exception as e:
        message = f"Failed to create superuser: {str(e)}"
        if verbose:
            print(f"Error: {message}")
        return False, message


def main():
    """Main function for standalone script execution."""
    setup_django()

    # Default credentials
    username = "admin"
    email = "admin@eventhorizon.local"
    password = "Ihapwics123$"
    first_name = "Administrator"
    last_name = "Staff"

    success, message = create_superuser(
        username=username,
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
        verbose=True,
    )

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
