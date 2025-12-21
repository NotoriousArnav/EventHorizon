# Event Horizon Python CLI Client

A command-line interface for interacting with the Event Horizon API. This CLI supports both API Key and OAuth2 authentication methods.

## Installation

### Requirements
- Python 3.12+
- `requests` library

### Setup

1. Install the required dependency:
```bash
pip install requests
```

2. Make the script executable (optional):
```bash
chmod +x eventhorizon_cli.py
```

## Authentication

The CLI supports two authentication methods:

### 1. API Key Authentication (Recommended for CLI)

First, generate an API key from the Event Horizon web interface:

1. Log in to Event Horizon: `http://localhost:8000`
2. Go to Profile → API Keys
3. Click "Generate New API Key"
4. Copy your API key (it will only be shown once!)

Then use it with the CLI:
```bash
python eventhorizon_cli.py --api-key YOUR_API_KEY profile
```

### 2. OAuth2 Token Authentication

If you have an OAuth2 access token, you can use it instead:

```bash
python eventhorizon_cli.py --token YOUR_ACCESS_TOKEN profile
```

## Usage

```bash
python eventhorizon_cli.py [--api-key KEY | --token TOKEN] [--base-url URL] [--json] COMMAND
```

### Global Options

- `--api-key KEY`: Authenticate using an API key
- `--token TOKEN`: Authenticate using an OAuth2 access token
- `--base-url URL`: Base URL of the Event Horizon API (default: `http://localhost:8000`)
- `--json`: Output raw JSON instead of formatted text

**Note**: You must provide either `--api-key` or `--token` for authentication.

## Commands

### Profile

Get the authenticated user's profile information:

```bash
python eventhorizon_cli.py --api-key YOUR_KEY profile
```

**Output:**
```
User Profile
══════════════════════════════════════
Username:        arnav
Email:           arnav@example.com
First Name:      Arnav
Last Name:       Developer
Date Joined:     2024-12-21
```

### Events

#### List Events

List all available events with pagination:

```bash
python eventhorizon_cli.py --api-key YOUR_KEY events list
```

**Options:**
- `--limit N`: Number of events per page (default: 10)
- `--offset N`: Starting offset for pagination (default: 0)

**Example:**
```bash
python eventhorizon_cli.py --api-key YOUR_KEY events list --limit 5 --offset 10
```

**Output:**
```
Events (Showing 5 results)
══════════════════════════════════════
ID: 1
Title: Django Conference 2025
Description: Annual Django developers conference
Start: 2025-03-15 09:00:00
End: 2025-03-17 18:00:00
Location: San Francisco, CA
Status: Published
──────────────────────────────────────
...
```

#### Get Event Details

Get detailed information about a specific event:

```bash
python eventhorizon_cli.py --api-key YOUR_KEY events get EVENT_ID
```

**Example:**
```bash
python eventhorizon_cli.py --api-key YOUR_KEY events get 1
```

**Output:**
```
Event Details
══════════════════════════════════════
ID: 1
Title: Django Conference 2025
Slug: django-conference-2025
Description: Annual Django developers conference
Start: 2025-03-15 09:00:00
End: 2025-03-17 18:00:00
Location: San Francisco, CA
Status: Published
Created: 2024-12-21 10:30:00
Updated: 2024-12-21 11:45:00
Creator: arnav
```

#### Create Event

Create a new event:

```bash
python eventhorizon_cli.py --api-key YOUR_KEY events create \
  --title "My Event" \
  --description "Event description" \
  --start "2025-06-01 10:00:00" \
  --end "2025-06-01 16:00:00" \
  --location "New York, NY"
```

**Required Options:**
- `--title TEXT`: Event title
- `--description TEXT`: Event description
- `--start DATETIME`: Start datetime (format: YYYY-MM-DD HH:MM:SS)
- `--end DATETIME`: End datetime (format: YYYY-MM-DD HH:MM:SS)

**Optional Options:**
- `--location TEXT`: Event location
- `--status STATUS`: Event status (draft/published, default: draft)

**Output:**
```
✅ Event created successfully!

Event Details
══════════════════════════════════════
ID: 42
Title: My Event
Slug: my-event
Description: Event description
Start: 2025-06-01 10:00:00
End: 2025-06-01 16:00:00
Location: New York, NY
Status: Draft
```

#### Update Event

Update an existing event (partial update):

```bash
python eventhorizon_cli.py --api-key YOUR_KEY events update EVENT_ID [OPTIONS]
```

**Example:**
```bash
python eventhorizon_cli.py --api-key YOUR_KEY events update 1 \
  --title "Updated Title" \
  --location "New Location"
```

**Optional Options:**
- `--title TEXT`: Event title
- `--description TEXT`: Event description
- `--location TEXT`: Event location
- `--start-time DATETIME`: Start datetime (ISO format)
- `--end-time DATETIME`: End datetime (ISO format)
- `--max-attendees N`: Maximum attendees

**Output:**
```
✅ Event updated successfully!
══════════════════════════════════════
🎯 Updated Title
ID: 1
Slug: updated-title
📍 Location: New Location
📅 Start: 2025-03-15 09:00:00
```

#### Delete Event

Delete an event:

```bash
python eventhorizon_cli.py --api-key YOUR_KEY events delete EVENT_ID [--force]
```

**Example:**
```bash
# With confirmation prompt
python eventhorizon_cli.py --api-key YOUR_KEY events delete 1

# Skip confirmation
python eventhorizon_cli.py --api-key YOUR_KEY events delete 1 --force
```

**Output:**
```
⚠️  Are you sure you want to delete event 1?
This action cannot be undone.
Type 'yes' to confirm: yes
🗑️  Deleting event 1...
✅ Event 1 deleted successfully
```

### Registrations

#### List My Registrations

View all your event registrations:

```bash
python eventhorizon_cli.py --api-key YOUR_KEY registrations list
```

**Output:**
```
✅ Found 3 registration(s)
══════════════════════════════════════

🎫 Registration ID: 5
   Event: Django Conference 2025
   Status: registered
   Registered: 2025-01-15 14:30:00

🎫 Registration ID: 7
   Event: Python Meetup
   Status: registered
   Registered: 2025-01-20 09:15:00
```

#### Register for Event

Register for an event:

```bash
python eventhorizon_cli.py --api-key YOUR_KEY registrations register EVENT_ID [--answers JSON]
```

**Example:**
```bash
# Simple registration
python eventhorizon_cli.py --api-key YOUR_KEY registrations register 1

# With registration answers
python eventhorizon_cli.py --api-key YOUR_KEY registrations register 1 \
  --answers '{"q1": "Software Engineer", "q2": "Python"}'
```

**Optional Options:**
- `--answers JSON`: Registration form answers (JSON string)

**Output:**
```
✅ Successfully registered!
══════════════════════════════════════
🎫 Registration ID: 42
Event: Django Conference 2025
Status: registered
Registered: 2025-01-21 10:00:00
```

#### Unregister from Event

Unregister from an event:

```bash
python eventhorizon_cli.py --api-key YOUR_KEY registrations unregister EVENT_ID
```

**Example:**
```bash
python eventhorizon_cli.py --api-key YOUR_KEY registrations unregister 1
```

**Output:**
```
✅ Successfully unregistered from event 1
```

#### View Event Attendees (Organizer Only)

View all attendees for your event:

```bash
python eventhorizon_cli.py --api-key YOUR_KEY registrations attendees EVENT_ID
```

**Example:**
```bash
python eventhorizon_cli.py --api-key YOUR_KEY registrations attendees 1
```

**Output:**
```
✅ Found 25 attendee(s)
══════════════════════════════════════

👤 johndoe
   Name: John Doe
   Email: john@example.com
   Status: registered
   Registered: 2025-01-15 14:30:00

👤 janesmith
   Name: Jane Smith
   Email: jane@example.com
   Status: registered
   Registered: 2025-01-16 09:00:00
```

**Note:** This command only works if you are the organizer of the event.

## JSON Output

For scripting or parsing purposes, use the `--json` flag to get raw JSON output:

```bash
python eventhorizon_cli.py --api-key YOUR_KEY --json events list
```

**Output:**
```json
{
  "count": 42,
  "next": "http://localhost:8000/api/events/?limit=10&offset=10",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Django Conference 2025",
      ...
    }
  ]
}
```

## Examples

### Get your profile
```bash
python eventhorizon_cli.py --api-key abc123 profile
```

### List first 20 events
```bash
python eventhorizon_cli.py --api-key abc123 events list --limit 20
```

### Get event details
```bash
python eventhorizon_cli.py --api-key abc123 events get 5
```

### Create a draft event
```bash
python eventhorizon_cli.py --api-key abc123 events create \
  --title "Python Meetup" \
  --description "Monthly Python user group meetup" \
  --start "2025-07-15 18:00:00" \
  --end "2025-07-15 21:00:00" \
  --location "Tech Hub, Seattle" \
  --status draft
```

### Update an event
```bash
python eventhorizon_cli.py --api-key abc123 events update 5 \
  --title "Updated Python Meetup" \
  --location "New Venue"
```

### Delete an event
```bash
python eventhorizon_cli.py --api-key abc123 events delete 5 --force
```

### Register for an event
```bash
python eventhorizon_cli.py --api-key abc123 registrations register 1
```

### List your registrations
```bash
python eventhorizon_cli.py --api-key abc123 registrations list
```

### Unregister from an event
```bash
python eventhorizon_cli.py --api-key abc123 registrations unregister 1
```

### View event attendees (as organizer)
```bash
python eventhorizon_cli.py --api-key abc123 registrations attendees 1
```

### Use with a different server
```bash
python eventhorizon_cli.py --base-url https://events.example.com --api-key abc123 profile
```

### Get JSON output for scripting
```bash
# Get event count
python eventhorizon_cli.py --api-key abc123 --json events list | jq '.count'

# Get all event titles
python eventhorizon_cli.py --api-key abc123 --json events list | jq '.results[].title'
```

## Error Handling

The CLI provides clear error messages:

```bash
# Authentication error
❌ Error: Authentication failed. Please check your API key or token.

# Not found error
❌ Error: Event not found (404)

# Validation error
❌ Error: Bad Request (400)
{
  "start": ["Start time must be before end time"]
}

# Network error
❌ Error: Failed to connect to the server. Is it running?
```

## Troubleshooting

### "No module named 'requests'"
Install the requests library:
```bash
pip install requests
```

### "Authentication failed"
- Make sure your API key or OAuth2 token is valid
- Check that you haven't revoked the API key in the web interface
- For OAuth2 tokens, ensure they haven't expired

### "Connection refused"
- Verify the Event Horizon server is running: `uv run python manage.py runserver`
- Check that the base URL is correct (default: `http://localhost:8000`)
- Use `--base-url` to specify a different URL if needed

### "Event not found"
- Verify the event ID exists by listing events first
- Make sure you have permission to access the event

## Development

### Adding New Commands

The CLI uses Python's `argparse` library with subcommands. To add a new command:

1. Define a new subparser in the `main()` function
2. Add the required arguments
3. Implement the command logic in a separate function
4. Add formatted output for user-friendly display

### Authentication Headers

The CLI automatically sets the correct authentication header:
- API Key: `Authorization: Token YOUR_API_KEY`
- OAuth2: `Authorization: Bearer YOUR_ACCESS_TOKEN`

## License

This example client is part of the Event Horizon project and is provided as-is for demonstration purposes.

## Support

For issues or questions:
- Check the main Event Horizon documentation: `/docs/`
- Review API documentation: `/docs/api/`
- Report bugs in the main project repository
