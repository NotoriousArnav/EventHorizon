# Registration System

The registration system manages the flow of users joining events.

## Registration Lifecycle

1.  **Initiation:** User clicks "Join Mission".
2.  **Validation:** System checks capacity and existing registration status.
3.  **Data Collection:** If the event has custom questions, the user is prompted to answer them.
4.  **Confirmation:**
    - If space is available -> **Registered**.
    - If full -> **Waitlisted**.

## Waitlist Mechanics

The waitlist is a First-In-First-Out (FIFO) queue, though currently manual promotion is the standard operating procedure.

- **Waitlisted** users do not count towards the active capacity.
- They can be viewed by the organizer in the "Manage Registrations" view.

## Cancellation

Users can withdraw from a mission at any time. This frees up a spot, potentially allowing a waitlisted user to be promoted (manual action required).
