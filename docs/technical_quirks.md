# Project Quirks & Architecture Notes

This document captures specific quirks, non-standard configurations, and implementation details observed in the EventHorizon project. It serves as a guide for developers to understand the "why" behind some of the unique architectural decisions.

## 1. Architectural Philosophy (The "Legacy Bridge")

*   **Hybrid Architecture:** The project is an "Enterprise-Grade" hybrid system designed to bridge modern Python/Django backends with legacy infrastructure.
*   **The "Satellite" Client:** The `examples/php-client/` directory isn't just an example; it's a "Legacy Bridge." It is explicitly coded in **Zero-Dependency PHP** (no Composer, no frameworks) to run on ancient servers (e.g., Windows Server 2008, LAMP stacks with PHP 7.x) that cannot host modern Python applications.
*   **Two-Tiered UX:**
    *   **Public Portal:** Modern, glassmorphic UI (Django + Tailwind) for attendees.
    *   **Admin Terminal:** A utilitarian, high-contrast PHP interface designed to mimic a command terminal and function on legacy browsers (even IE7).

## 2. Environment & Initialization

*   **Custom `init_project.py`:** Instead of a standard `requirements.txt` install, the project uses a custom Python script that:
    *   Auto-detects `uv` for dependency management (but falls back to `pip`).
    *   Generates a secure `.env` file with secrets and debug settings.
    *   Prompts to run migrations and create a superuser interactively.
*   **Dependency Management:** Strong preference for `uv` ("lightning-fast"), with specific checks for `uv.lock`.
*   **`main.py` vs `manage.py`:** There is a `main.py` file that simply prints "Hello from eventhorizon!". It appears to be a placeholder or artifact, as the actual entry point is the standard Django `manage.py`.

## 3. Authentication & Security

*   **Dual Auth Backends:** Configured to use both the standard Django ModelBackend and `allauth`'s AuthenticationBackend simultaneously.
*   **Complex API Auth:** The API accepts **both** OAuth2 tokens (for the PHP client/external apps) and Knox tokens (likely for the frontend), which is an unusual dual-stack configuration.
*   **Hardcoded OIDC Issuer:** The OpenID Connect issuer is hardcoded to `http://127.0.0.1:8000/o` in `settings.py`. This is a "fragile" configuration that will break if deployed to a domain without updating settings.
*   **Superuser Script:** `create_superuser.py` contains hardcoded credentials (`admin` / `Ihapwics123$`). This is a convenience script but represents a security risk if accidentally deployed.

## 4. Data Modeling

*   **NoSQL in SQL:** The `Event` and `Registration` models use `JSONField` to implement a dynamic form builder (`registration_schema` and `answers`). This allows organizers to define custom questions per event without schema migrations.
*   **Manual Slugification:** The `Event` model uses a custom `save()` method with a `while` loop to ensure unique slugs (e.g., `event-title-1`, `event-title-2`) rather than using a standard library like `django-autoslug`.

## 5. Frontend & UI

*   **CDN-based Tailwind:** Tailwind CSS is loaded via CDN in `base.html` rather than a local build process. This favors rapid prototyping ("Launch Sequence") over production performance.
*   **Sci-Fi Aesthetic:** The project explicitly uses "Rajdhani" and "Inter" fonts and specific color palettes (`#0B0C10`, `#66FCF1`) to enforce a futuristic "Event Horizon" theme.

## 6. URL Routing

*   **Root Overlap:** Both `events` and `home` apps are included at the root path (`""`). Since `events.urls` is loaded first, it takes precedence. This relies on the fact that `events.urls` *doesn't* have a root path `""` defined, allowing requests to fall through to `home.urls`. This is implicit and brittle routing logic.
