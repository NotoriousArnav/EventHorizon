# API Reference

The Event Horizon API allows external applications to interact with the platform. It is built using **Django REST Framework (DRF)**.

**Base URL:** `/` (e.g., `http://127.0.0.1:8000/`)

## Authentication

The API uses **OAuth 2.0**. Clients must obtain an `access_token` via the Authorization Code Flow (with PKCE).
Once obtained, the token must be included in the header of all requests:

```http
Authorization: Bearer <your_access_token>
```

---

## Users

### Get Current User Profile

Retrieves the profile information of the currently authenticated user.

*   **Endpoint:** `/accounts/api/me/`
*   **Method:** `GET`
*   **Permissions:** Authenticated User

#### Response Example

```json
{
  "id": 1,
  "username": "commander_shepard",
  "email": "shepard@alliance.navy",
  "first_name": "John",
  "last_name": "Shepard",
  "date_joined": "2183-04-11T10:00:00Z",
  "profile": {
    "bio": "Spectre. Commander of the Normandy.",
    "location": "Citadel",
    "phone_number": "555-0199",
    "avatar": "/media/avatars/shepard.jpg",
    "social_links": [
      {
        "platform": "github",
        "url": "https://github.com/spectre"
      }
    ]
  }
}
```

---

## Events (Planned / In-Development)

*Note: The Events API is currently under active development. The following specification is based on the underlying data models and serializers.*

### List Events

*   **Endpoint:** `/api/events/` (Proposed)
*   **Method:** `GET`
*   **Query Parameters:**
    *   `search`: Search by title or description.
    *   `location`: Filter by location.

#### Response Example

```json
[
  {
    "id": 101,
    "title": "Operation: Skyfall",
    "description": "High altitude drop mission.",
    "start_time": "2025-12-20T14:00:00Z",
    "end_time": "2025-12-20T18:00:00Z",
    "location": "Sector 7",
    "capacity": 50,
    "organizer": {
      "id": 5,
      "username": "admiral_hacket",
      "email": "hacket@alliance.navy"
    },
    "is_registered": false
  }
]
```

### Event Registration

*   **Endpoint:** `/api/events/{id}/register/` (Proposed)
*   **Method:** `POST`
*   **Body:**
    *   `answers`: JSON object containing answers to registration questions (if any).

```json
{
  "answers": {
    "q_1": "Pilot",
    "q_2": "Yes"
  }
}
```
