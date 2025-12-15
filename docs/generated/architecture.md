# Architecture Overview

## High-Level Structure

Event Horizon is a monolithic web application built on the **Django** framework (Python). It adheres to the Model-View-Template (MVT) architectural pattern, enhanced with **Django REST Framework** for API capabilities and **Tailwind CSS** for the frontend interface.

### Key Components

1.  **Core Application (`EventHorizon/`)**: Handles project-wide settings, URL routing, and WSGI/ASGI configuration.
2.  **Events Module (`events/`)**: The heart of the system. Manages event creation, listing, details, and the registration logic (including waitlists and capacity checks).
3.  **Users Module (`users/`)**: Extends the default Django authentication system. Manages user profiles, social links, and API-based user data retrieval.
4.  **Home Module (`home/`)**: Landing page and static content delivery.
5.  **Templates (`templates/`)**: HTML files rendered by Django, styled with utility-first Tailwind CSS classes.

## Tech Stack

### Backend
*   **Framework:** Django 6.0
*   **Language:** Python 3.10+
*   **Database:** SQLite (Default, adaptable to PostgreSQL)
*   **API:** Django REST Framework (DRF)
*   **Authentication:** `django-allauth` (Social/Local auth) & `django-oauth-toolkit` (OAuth2 Provider)

### Frontend
*   **Styling:** Tailwind CSS (via CDN for simplicity, configurable for build pipeline)
*   **UI Philosophy:** Glassmorphism, Dark Mode, Terminal/Sci-Fi Aesthetic

### Infrastructure & Tooling
*   **Dependency Management:** `uv` (recommended) or `pip`
*   **Environment Config:** `python-dotenv`
*   **CI/CD:** GitHub Actions (Automated testing on push/PR)

## Security Architecture

*   **OAuth 2.0 / OIDC:** The platform acts as an OAuth2 provider, allowing external clients (like the PHP CLI) to authenticate users securely via PKCE (Proof Key for Code Exchange) flow.
*   **CSRF Protection:** Standard Django CSRF middleware is active for all form submissions.
*   **Authentication:** Session-based auth for web users; Token-based (Bearer) for API clients.

## Data Flow

1.  **User Request:** Enters via Nginx/Gunicorn (prod) or `runserver` (dev).
2.  **URL Routing:** Dispatches request to appropriate View (MVT) or ViewSet (API).
3.  **Logic Layer:** Views interact with Models (ORM) to fetch/manipulate data.
4.  **Presentation:**
    *   **Web:** Views render HTML Templates.
    *   **API:** Serializers convert Model instances to JSON.
5.  **Response:** HTML or JSON returned to client.
