# Developer Guide

## System Requirements

*   Python 3.10 or higher
*   Git
*   `uv` (Recommended) or `pip`

## Installation

1.  **Clone the Repository:**
    ```bash
    git clone <repository_url>
    cd EventHorizon
    ```

2.  **Initialize Environment:**
    We provide a helper script to automate setup (venv creation, dependencies, .env file).
    ```bash
    # If you have uv installed (Recommended)
    uv run init_project.py

    # OR with standard python
    python init_project.py
    ```

3.  **Manual Setup (Alternative):**
    ```bash
    # Install dependencies
    uv sync  # or pip install -r requirements.txt

    # Apply migrations
    python manage.py migrate

    # Create Superuser
    python manage.py createsuperuser
    ```

## Running the Development Server

```bash
python manage.py runserver
```
Access the application at `http://127.0.0.1:8000`.

## Project Structure

*   `EventHorizon/`: Core Django settings (`settings.py`, `urls.py`).
*   `events/`: Main application logic.
    *   `models.py`: `Event`, `Registration` models.
    *   `views.py`: Class-Based Views (CBVs) for UI.
    *   `serializers.py`: DRF serializers for API.
*   `users/`: Custom user handling.
    *   `api_views.py`: API endpoints for user data.
*   `templates/`: HTML templates using Tailwind CSS.

## Testing

Run the test suite to ensure system integrity:

```bash
python manage.py test
```

## Contributing

1.  **Branching Strategy:** Use feature branches (`feature/new-scanner`) off `main`.
2.  **Code Style:** Follow PEP 8.
3.  **Pull Requests:** Submit PRs to `main`. Ensure CI checks pass.
