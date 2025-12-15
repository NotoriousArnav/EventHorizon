# API Endpoints

## Events

### List Events
`GET /api/events/`
- **Query Params:** `search` (Title/Location)
- **Response:** Array of Event objects.

### Create Event
`POST /api/events/`
- **Body:**
  ```json
  {
      "title": "Mission Alpha",
      "description": "Briefing...",
      "start_time": "2025-01-01T10:00:00Z",
      "end_time": "2025-01-01T12:00:00Z",
      "location": "Sector 7",
      "capacity": 50
  }
  ```

### Get Event Detail
`GET /api/events/{id}/`
- **Response:** Event object with `organizer` details.

## Registrations

### Register for Event
`POST /api/events/{id}/register/`
- **Body:**
  ```json
  {
      "answers": {
          "q1": "Answer text"
      }
  }
  ```

### Cancel Registration
`DELETE /api/events/{id}/register/`

## Users

### Get Current User
`GET /accounts/api/me/`
- **Response:**
  ```json
  {
      "id": 1,
      "username": "cmdr_shepard",
      "email": "shepard@alliance.navy",
      "first_name": "Jane",
      "last_name": "Shepard"
  }
  ```
