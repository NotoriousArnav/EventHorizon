# Event Horizon - Documentation

## Overview

Event Horizon is a Django-based event management platform with a futuristic "Deep Space / Command Terminal" aesthetic. It allows users to create events ("Missions"), register for them, manage waitlists, and customize registration forms.

## Key Features

### 1. Mission Control (Events)
- **Create Missions:** Organizers can initialize new events with title, description, time, location, and capacity.
- **Custom Registration Forms:** Organizers can define custom data requirements (questions) for attendees (Text, Checkbox, Long Text).
- **Search & Filter:** Users can scan for missions by ID, Title, or Sector (Location).

### 2. Personnel Management (Users)
- **Authentication:** Secure login/signup via `django-allauth`.
- **Profiles:** Users have "Command Profiles" with avatars and bios.
- **Dashboard:** "My Missions" view separates hosted events ("Command Logs") from attended events ("Mission Assignments").

### 3. Registration System
- **Capacity Handling:** Automatic waitlisting when capacity is full.
- **Status Tracking:** Users can see if they are `Active`, `Waitlisted`, or `Cancelled`.
- **Notifications:** Email notifications (currently Console Backend) for status changes.
- **Data Collection:** Collects answers to custom organizer questions during registration.

## Tech Stack

- **Backend:** Django 6.0, SQLite
- **Frontend:** Tailwind CSS (CDN), Custom Glassmorphism UI
- **Utilities:** `python-dotenv` for secrets, `django-crispy-forms` (optional/integrated manually).

## Setup & Installation

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/yourusername/EventHorizon.git
    cd EventHorizon
    ```

2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    # OR using uv
    uv sync
    ```

3.  **Environment Variables:**
    Create a `.env` file in the root:
    ```env
    DEBUG=True
    SECRET_KEY=your-secret-key-here
    ```

4.  **Run Migrations:**
    ```bash
    python manage.py migrate
    ```

5.  **Start Server:**
    ```bash
    python manage.py runserver
    ```

## Project Structure

- `EventHorizon/`: Project settings and configuration.
- `home/`: Homepage and general views.
- `users/`: User profiles and authentication extensions.
- `events/`: Core event logic, models, and views.
- `templates/`: HTML templates with Tailwind styling.
- `theme/`: (Optional) Tailwind configuration if using standalone build.
