# Mission Control (Events)

Mission Control is the core module for managing events in Event Horizon.

## Creating a Mission

Commanders (Organizers) can initialize missions via the dashboard.

**Required Fields:**
- **Title:** The operational name of the event.
- **Description:** Briefing details.
- **Start/End Time:** Temporal coordinates.
- **Location:** Physical or virtual sector.
- **Capacity:** Maximum crew complement.

## Custom Registration Schema

Organizers can define custom data requirements for registration. This is stored as a JSON schema.

**Supported Question Types:**
1.  **Text:** Short answer (e.g., "Callsign").
2.  **Long Text:** Detailed response (e.g., "Mission Motivation").
3.  **Checkbox:** Boolean confirmation (e.g., "Agree to Terms").

## Waitlist Protocol

When a mission reaches full capacity:
1.  New registrants are automatically assigned `Waitlisted` status.
2.  If a `Registered` user cancels, a waitlisted user is **not** automatically promoted (currently manual promotion is required by the organizer, or via API).

## Event Slugs

Every event is assigned a unique URL-friendly `slug` (e.g., `operation-red-sun-2`). This is used for sharing public links.
