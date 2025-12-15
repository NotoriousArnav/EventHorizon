# API Overview

Event Horizon provides a RESTful API powered by **Django REST Framework (DRF)**.

## Base URL
```
http://<your-domain>/api/
```

## Authentication
The API supports **OAuth2** (Bearer Token) and **Session Authentication** (for browser-based interaction).

## Core Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/events/` | List all events. |
| `POST` | `/events/` | Create a new event (Auth required). |
| `GET` | `/events/{id}/` | Get details of a specific event. |
| `POST` | `/events/{id}/register/` | Register for an event. |
| `GET` | `/users/me/` | Get current user profile. |

## Error Handling
Standard HTTP status codes are used:
- `200 OK`: Success.
- `201 Created`: Resource created.
- `400 Bad Request`: Validation error.
- `401 Unauthorized`: Authentication missing/invalid.
- `403 Forbidden`: Permission denied.
- `404 Not Found`: Resource does not exist.
