# Personnel (Users & Auth)

The user management system handles identities, profiles, and access control.

## Authentication
Event Horizon uses `django-allauth` for robust authentication.

- **Signup:** Email verification is supported (optional).
- **Login:** Standard username/password or social login (configurable).
- **Password Reset:** Built-in flow for lost credentials.

## Command Profiles
Every user has a profile that extends the standard Django User model.

**Profile Fields:**
- **Avatar:** Profile picture (Command Identity).
- **Bio:** Short description or service record.
- **Social Links:** Links to external communication channels (GitHub, Twitter, etc.).

## Dashboard
The dashboard acts as the user's home base.
- **My Missions:** Events the user has registered for.
- **Command Logs:** Events the user is hosting.
- **Settings:** Update profile information and account settings.
