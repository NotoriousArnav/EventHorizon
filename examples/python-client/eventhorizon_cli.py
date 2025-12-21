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
Event Horizon API CLI Client

A command-line utility to interact with the Event Horizon API.
Demonstrates authentication (API Key and OAuth2) and basic API operations.

Usage:
    python eventhorizon_cli.py --help
    python eventhorizon_cli.py --api-key YOUR_KEY profile
    python eventhorizon_cli.py --api-key YOUR_KEY events list
    python eventhorizon_cli.py --api-key YOUR_KEY events get <event-id>
    python eventhorizon_cli.py --api-key YOUR_KEY events create --title "Event" --start-time ... --end-time ...
    python eventhorizon_cli.py --api-key YOUR_KEY events update <event-id> --title "New Title"
    python eventhorizon_cli.py --api-key YOUR_KEY events delete <event-id>
    python eventhorizon_cli.py --api-key YOUR_KEY registrations list
    python eventhorizon_cli.py --api-key YOUR_KEY registrations register <event-id>
    python eventhorizon_cli.py --api-key YOUR_KEY registrations unregister <event-id>
    python eventhorizon_cli.py --api-key YOUR_KEY registrations attendees <event-id>
"""

import argparse
import sys
import json
import requests
from typing import Optional, Dict, Any
from urllib.parse import urljoin


class EventHorizonClient:
    """Client for interacting with Event Horizon API"""

    def __init__(
        self,
        base_url: str = "http://127.0.0.1:8000",
        api_key: Optional[str] = None,
        oauth_token: Optional[str] = None,
    ):
        """
        Initialize the API client.

        Args:
            base_url: Base URL of the Event Horizon instance
            api_key: Knox API key for authentication
            oauth_token: OAuth2 access token for authentication
        """
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()

        # Set authentication headers
        if api_key:
            self.session.headers["Authorization"] = f"Token {api_key}"
        elif oauth_token:
            self.session.headers["Authorization"] = f"Bearer {oauth_token}"

        self.session.headers["Content-Type"] = "application/json"
        self.session.headers["Accept"] = "application/json"

    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[Any, Any]:
        """
        Make an HTTP request to the API.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint path
            **kwargs: Additional arguments to pass to requests

        Returns:
            Response JSON data

        Raises:
            SystemExit: If request fails
        """
        url = urljoin(self.base_url, endpoint)

        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()

            # Return JSON if available
            if response.text:
                return response.json()
            return {}

        except requests.exceptions.HTTPError as e:
            print(f"❌ HTTP Error: {e}")
            if hasattr(e.response, "text"):
                print(f"Response: {e.response.text}")
            sys.exit(1)
        except requests.exceptions.ConnectionError:
            print(f"❌ Connection Error: Could not connect to {self.base_url}")
            print("Make sure the Event Horizon server is running.")
            sys.exit(1)
        except requests.exceptions.RequestException as e:
            print(f"❌ Request Error: {e}")
            sys.exit(1)

    def get_profile(self) -> Dict[Any, Any]:
        """Get the authenticated user's profile"""
        return self._make_request("GET", "/accounts/api/me/")

    def list_events(self, page: int = 1) -> Dict[Any, Any]:
        """List all events"""
        return self._make_request("GET", f"/api/events/?page={page}")

    def get_event(self, event_id: int) -> Dict[Any, Any]:
        """Get a specific event by ID"""
        return self._make_request("GET", f"/api/events/{event_id}/")

    def create_event(self, data: Dict[Any, Any]) -> Dict[Any, Any]:
        """Create a new event"""
        return self._make_request("POST", "/api/events/", json=data)

    def update_event(self, event_id: int, data: Dict[Any, Any]) -> Dict[Any, Any]:
        """Update an existing event (partial update)"""
        return self._make_request("PATCH", f"/api/events/{event_id}/", json=data)

    def delete_event(self, event_id: int) -> None:
        """Delete an event"""
        self._make_request("DELETE", f"/api/events/{event_id}/")
        print(f"✅ Event {event_id} deleted successfully")

    def register_for_event(
        self, event_id: int, answers: Optional[Dict[Any, Any]] = None
    ) -> Dict[Any, Any]:
        """Register the current user for an event"""
        data = {"answers": answers or {}}
        return self._make_request(
            "POST", f"/api/events/{event_id}/register/", json=data
        )

    def unregister_from_event(self, event_id: int) -> None:
        """Unregister the current user from an event"""
        self._make_request("POST", f"/api/events/{event_id}/unregister/")
        print(f"✅ Successfully unregistered from event {event_id}")

    def list_my_registrations(self) -> Dict[Any, Any]:
        """List the current user's registrations"""
        return self._make_request("GET", "/api/registrations/")

    def get_event_registrations(self, event_id: int) -> Dict[Any, Any]:
        """Get all registrations for an event (organizer only)"""
        return self._make_request("GET", f"/api/events/{event_id}/registrations/")


def format_json(data: Any, indent: int = 2) -> str:
    """Format data as pretty JSON"""
    return json.dumps(data, indent=indent, ensure_ascii=False)


def handle_profile(client: EventHorizonClient, args: argparse.Namespace):
    """Handle profile command"""
    print("📋 Fetching user profile...")
    profile = client.get_profile()

    print("\n✅ Profile retrieved successfully!")
    print("=" * 60)
    print(f"Username:  {profile.get('username', 'N/A')}")
    print(f"Email:     {profile.get('email', 'N/A')}")
    print(f"First Name: {profile.get('first_name', 'N/A')}")
    print(f"Last Name:  {profile.get('last_name', 'N/A')}")

    if profile.get("profile"):
        print(f"\n📍 Location: {profile['profile'].get('location', 'N/A')}")
        print(f"📱 Phone:    {profile['profile'].get('phone_number', 'N/A')}")
        if profile["profile"].get("bio"):
            print(f"\n💭 Bio:\n{profile['profile']['bio']}")

    if args.json:
        print("\n" + "=" * 60)
        print("JSON Response:")
        print(format_json(profile))


def handle_events_list(client: EventHorizonClient, args: argparse.Namespace):
    """Handle events list command"""
    data = client.list_events(page=args.page)
    events = data  # .get("results", [])

    if args.json:
        print(format_json(data))
        return

    print(f"📅 Fetching events (page {args.page})...")
    if not events:
        print("No events found.")
        return

    print(f"\n✅ Found {len(events)} total events")
    print("=" * 60)

    for event in events:
        print(f"\n🎯 {event.get('title', 'Untitled')}")
        print(f"   ID: {event.get('id')}")
        print(f"   📍 Location: {event.get('location', 'N/A')}")
        print(f"   📅 Start: {event.get('start_time', 'N/A')}")
        print(f"   👤 Organizer: {event.get('organizer', {}).get('username', 'N/A')}")
        print(
            f"   👥 Capacity: {event.get('current_attendees', 0)}/{event.get('capacity', 'unlimited')}"
        )

        if event.get("description"):
            desc = event["description"][:100]
            if len(event["description"]) > 100:
                desc += "..."
            print(f"   📝 {desc}")

    # # Pagination info
    # if data.get("next"):
    #     print(f"\n➡️  More events available. Use --page {args.page + 1}")


def handle_events_get(client: EventHorizonClient, args: argparse.Namespace):
    """Handle events get command"""
    print(f"📅 Fetching event {args.event_id}...")
    event = client.get_event(args.event_id)

    print("\n✅ Event retrieved successfully!")
    print("=" * 60)
    print(f"🎯 {event.get('title', 'Untitled')}")
    print(f"ID: {event.get('id')}")
    print(f"Slug: {event.get('slug', 'N/A')}")
    print(f"\n📍 Location: {event.get('location', 'N/A')}")
    print(f"📅 Start: {event.get('start_time', 'N/A')}")
    print(f"📅 End: {event.get('end_time', 'N/A')}")
    print(f"\n👤 Organizer: {event.get('organizer', {}).get('username', 'N/A')}")
    print(
        f"👥 Capacity: {event.get('current_attendees', 0)}/{event.get('max_attendees', 'unlimited')}"
    )
    print(f"📊 Status: {event.get('status', 'N/A')}")

    if event.get("description"):
        print(f"\n📝 Description:\n{event['description']}")

    if event.get("registration_schema"):
        print(f"\n📋 Registration Schema:")
        print(format_json(event["registration_schema"]))

    if args.json:
        print("\n" + "=" * 60)
        print("JSON Response:")
        print(format_json(event))


def handle_events_create(client: EventHorizonClient, args: argparse.Namespace):
    """Handle events create command"""
    print("📝 Creating new event...")

    # Build event data
    event_data = {
        "title": args.title,
        "description": args.description or "",
        "location": args.location or "",
        "start_time": args.start_time,
        "end_time": args.end_time,
    }

    if args.max_attendees:
        event_data["capacity"] = args.max_attendees

    if args.registration_schema:
        try:
            event_data["registration_schema"] = json.loads(args.registration_schema)
        except json.JSONDecodeError:
            print("❌ Invalid JSON in --registration-schema")
            sys.exit(1)

    event = client.create_event(event_data)

    print("\n✅ Event created successfully!")
    print("=" * 60)
    print(f"🎯 {event.get('title')}")
    print(f"ID: {event.get('id')}")
    print(f"Slug: {event.get('slug')}")
    print(f"📍 Location: {event.get('location')}")
    print(f"📅 Start: {event.get('start_time')}")

    if args.json:
        print("\n" + "=" * 60)
        print("JSON Response:")
        print(format_json(event))


def handle_events_update(client: EventHorizonClient, args: argparse.Namespace):
    """Handle events update command"""
    print(f"✏️  Updating event {args.event_id}...")

    # Build event data with only provided fields (PATCH allows partial updates)
    event_data = {}

    if args.title:
        event_data["title"] = args.title
    if args.description is not None:
        event_data["description"] = args.description
    if args.location is not None:
        event_data["location"] = args.location
    if args.start_time:
        event_data["start_time"] = args.start_time
    if args.end_time:
        event_data["end_time"] = args.end_time
    if args.max_attendees:
        event_data["max_attendees"] = args.max_attendees
    if args.registration_schema:
        try:
            event_data["registration_schema"] = json.loads(args.registration_schema)
        except json.JSONDecodeError:
            print("❌ Invalid JSON in --registration-schema")
            sys.exit(1)

    if not event_data:
        print("❌ No fields to update. Please provide at least one field to update.")
        sys.exit(1)

    event = client.update_event(args.event_id, event_data)

    print("\n✅ Event updated successfully!")
    print("=" * 60)
    print(f"🎯 {event.get('title')}")
    print(f"ID: {event.get('id')}")
    print(f"Slug: {event.get('slug')}")
    print(f"📍 Location: {event.get('location')}")
    print(f"📅 Start: {event.get('start_time')}")

    if args.json:
        print("\n" + "=" * 60)
        print("JSON Response:")
        print(format_json(event))


def handle_events_delete(client: EventHorizonClient, args: argparse.Namespace):
    """Handle events delete command"""
    # Confirm deletion unless --force is provided
    if not args.force:
        print(f"⚠️  Are you sure you want to delete event {args.event_id}?")
        print("This action cannot be undone.")
        response = input("Type 'yes' to confirm: ")
        if response.lower() != "yes":
            print("❌ Deletion cancelled.")
            sys.exit(0)

    print(f"🗑️  Deleting event {args.event_id}...")
    client.delete_event(args.event_id)
    # Success message is printed by the client method


def handle_registrations_list(client: EventHorizonClient, args: argparse.Namespace):
    """Handle registrations list command"""
    print("📋 Fetching your registrations...")
    data = client.list_my_registrations()

    registrations = data.get("results", [])

    if not registrations:
        print("You have no event registrations.")
        return

    print(f"\n✅ Found {len(registrations)} registration(s)")
    print("=" * 60)

    for reg in registrations:
        print(f"\n🎫 Registration ID: {reg.get('id')}")
        print(f"   Event: {reg.get('event_title', 'N/A')}")
        print(f"   Status: {reg.get('status', 'N/A')}")
        print(f"   Registered: {reg.get('registered_at', 'N/A')}")

    if args.json:
        print("\n" + "=" * 60)
        print("JSON Response:")
        print(format_json(data))


def handle_registrations_register(client: EventHorizonClient, args: argparse.Namespace):
    """Handle event registration command"""
    print(f"📝 Registering for event {args.event_id}...")

    # Parse answers if provided
    answers = {}
    if args.answers:
        try:
            answers = json.loads(args.answers)
        except json.JSONDecodeError:
            print("❌ Invalid JSON in --answers")
            sys.exit(1)

    registration = client.register_for_event(args.event_id, answers)

    print("\n✅ Successfully registered!")
    print("=" * 60)
    print(f"🎫 Registration ID: {registration.get('id')}")
    print(f"Event: {registration.get('event_title', 'N/A')}")
    print(f"Status: {registration.get('status', 'N/A')}")
    print(f"Registered: {registration.get('registered_at', 'N/A')}")

    if args.json:
        print("\n" + "=" * 60)
        print("JSON Response:")
        print(format_json(registration))


def handle_registrations_unregister(
    client: EventHorizonClient, args: argparse.Namespace
):
    """Handle event unregistration command"""
    print(f"🗑️  Unregistering from event {args.event_id}...")
    client.unregister_from_event(args.event_id)
    # Success message is printed by the client method


def handle_registrations_attendees(
    client: EventHorizonClient, args: argparse.Namespace
):
    """Handle view event attendees command (organizer only)"""
    print(f"👥 Fetching attendees for event {args.event_id}...")
    registrations = client.get_event_registrations(args.event_id)

    if not registrations:
        print("No registrations found for this event.")
        return

    print(f"\n✅ Found {len(registrations)} attendee(s)")
    print("=" * 60)

    for reg in registrations:
        participant = reg.get("participant_info", {})
        print(f"\n👤 {participant.get('username', 'N/A')}")
        print(
            f"   Name: {participant.get('first_name', '')} {participant.get('last_name', '')}"
        )
        print(f"   Email: {participant.get('email', 'N/A')}")
        print(f"   Status: {reg.get('status', 'N/A')}")
        print(f"   Registered: {reg.get('registered_at', 'N/A')}")

    if args.json:
        print("\n" + "=" * 60)
        print("JSON Response:")
        print(format_json(registrations))


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Event Horizon API CLI Client",
        epilog="Examples:\n"
        "  %(prog)s --api-key YOUR_KEY profile\n"
        "  %(prog)s --api-key YOUR_KEY events list\n"
        "  %(prog)s --api-key YOUR_KEY events get 1\n",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    # Global options
    parser.add_argument(
        "--base-url",
        default="http://127.0.0.1:8000",
        help="Base URL of Event Horizon instance (default: http://127.0.0.1:8000)",
    )
    parser.add_argument("--api-key", help="Knox API key for authentication")
    parser.add_argument("--oauth-token", help="OAuth2 access token for authentication")
    parser.add_argument("--json", action="store_true", help="Output raw JSON response")

    # Subcommands
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Profile command
    profile_parser = subparsers.add_parser(
        "profile", help="Get authenticated user profile"
    )

    # Events commands
    events_parser = subparsers.add_parser("events", help="Manage events")
    events_subparsers = events_parser.add_subparsers(
        dest="events_command", help="Events operations"
    )

    # Events list
    list_parser = events_subparsers.add_parser("list", help="List all events")
    list_parser.add_argument(
        "--page", type=int, default=1, help="Page number (default: 1)"
    )

    # Events get
    get_parser = events_subparsers.add_parser("get", help="Get a specific event")
    get_parser.add_argument("event_id", type=int, help="Event ID")

    # Events create
    create_parser = events_subparsers.add_parser("create", help="Create a new event")
    create_parser.add_argument("--title", required=True, help="Event title")
    create_parser.add_argument("--description", help="Event description")
    create_parser.add_argument("--location", help="Event location")
    create_parser.add_argument(
        "--start-time",
        required=True,
        help="Start time (ISO format: 2024-12-25T10:00:00Z)",
    )
    create_parser.add_argument(
        "--end-time", required=True, help="End time (ISO format: 2024-12-25T12:00:00Z)"
    )
    create_parser.add_argument("--max-attendees", type=int, help="Maximum attendees")
    create_parser.add_argument(
        "--registration-schema", help="Registration schema (JSON string)"
    )

    # Events update
    update_parser = events_subparsers.add_parser(
        "update", help="Update an existing event"
    )
    update_parser.add_argument("event_id", type=int, help="Event ID")
    update_parser.add_argument("--title", help="Event title")
    update_parser.add_argument("--description", help="Event description")
    update_parser.add_argument("--location", help="Event location")
    update_parser.add_argument(
        "--start-time", help="Start time (ISO format: 2024-12-25T10:00:00Z)"
    )
    update_parser.add_argument(
        "--end-time", help="End time (ISO format: 2024-12-25T12:00:00Z)"
    )
    update_parser.add_argument("--max-attendees", type=int, help="Maximum attendees")
    update_parser.add_argument(
        "--registration-schema", help="Registration schema (JSON string)"
    )

    # Events delete
    delete_parser = events_subparsers.add_parser("delete", help="Delete an event")
    delete_parser.add_argument("event_id", type=int, help="Event ID")
    delete_parser.add_argument(
        "--force", action="store_true", help="Skip confirmation prompt"
    )

    # Registrations commands
    registrations_parser = subparsers.add_parser(
        "registrations", help="Manage event registrations"
    )
    registrations_subparsers = registrations_parser.add_subparsers(
        dest="registrations_command", help="Registration operations"
    )

    # Registrations list (my registrations)
    reg_list_parser = registrations_subparsers.add_parser(
        "list", help="List your registrations"
    )

    # Registrations register
    reg_register_parser = registrations_subparsers.add_parser(
        "register", help="Register for an event"
    )
    reg_register_parser.add_argument("event_id", type=int, help="Event ID")
    reg_register_parser.add_argument(
        "--answers", help="Registration answers (JSON string)"
    )

    # Registrations unregister
    reg_unregister_parser = registrations_subparsers.add_parser(
        "unregister", help="Unregister from an event"
    )
    reg_unregister_parser.add_argument("event_id", type=int, help="Event ID")

    # Registrations attendees (view event attendees - organizer only)
    reg_attendees_parser = registrations_subparsers.add_parser(
        "attendees", help="View event attendees (organizer only)"
    )
    reg_attendees_parser.add_argument("event_id", type=int, help="Event ID")

    args = parser.parse_args()

    # Check authentication
    if not args.api_key and not args.oauth_token:
        print("❌ Error: Authentication required!")
        print("Please provide either --api-key or --oauth-token")
        print("\nTo generate an API key:")
        print("  1. Log in to Event Horizon")
        print("  2. Go to API Keys page")
        print("  3. Click 'Generate New Key'")
        print("  4. Copy the key and use it with --api-key")
        sys.exit(1)

    # Check command
    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Initialize client
    client = EventHorizonClient(
        base_url=args.base_url, api_key=args.api_key, oauth_token=args.oauth_token
    )

    # Route to appropriate handler
    try:
        if args.command == "profile":
            handle_profile(client, args)
        elif args.command == "events":
            if args.events_command == "list":
                handle_events_list(client, args)
            elif args.events_command == "get":
                handle_events_get(client, args)
            elif args.events_command == "create":
                handle_events_create(client, args)
            elif args.events_command == "update":
                handle_events_update(client, args)
            elif args.events_command == "delete":
                handle_events_delete(client, args)
            else:
                events_parser.print_help()
        elif args.command == "registrations":
            if args.registrations_command == "list":
                handle_registrations_list(client, args)
            elif args.registrations_command == "register":
                handle_registrations_register(client, args)
            elif args.registrations_command == "unregister":
                handle_registrations_unregister(client, args)
            elif args.registrations_command == "attendees":
                handle_registrations_attendees(client, args)
            else:
                registrations_parser.print_help()
        else:
            parser.print_help()
    except KeyboardInterrupt:
        print("\n\n⚠️  Operation cancelled by user")
        sys.exit(130)


if __name__ == "__main__":
    main()
