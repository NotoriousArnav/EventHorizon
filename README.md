# Event Horizon

![Event Horizon Banner](https://img.shields.io/badge/Status-Operational-blue?style=for-the-badge) ![Django](https://img.shields.io/badge/Django-6.0-green?style=for-the-badge) ![Tailwind](https://img.shields.io/badge/Tailwind-CSS-blueviolet?style=for-the-badge)

**Event Horizon** is a next-generation event management platform designed with a futuristic "Command Terminal" aesthetic. It enables seamless mission planning (event creation), crew assembly (registration), and status tracking.

## 🚀 Features

*   **Immersive UI:** Glassmorphism, deep space backgrounds, and terminal-style typography using Tailwind CSS.
*   **Mission Control:** Organizers can create events with custom registration protocols (custom questions).
*   **Crew Management:**
    *   Dynamic waitlisting system.
    *   Approval/Cancellation workflows.
    *   Email notifications (Console backend).
*   **User Dashboard:**
    *   **Command Logs:** Manage events you are hosting.
    *   **Mission Assignments:** Track status of events you are attending.
*   **Search & Navigation:** Filter missions by sector (location) or codename (title).
*   **Flexible Database Support:** SQLite (default), PostgreSQL, MySQL via `DATABASE_URL` environment variable.
*   **S3-Compatible Storage:** Support for AWS S3, MinIO, DigitalOcean Spaces, and Cloudflare R2.

## 🛠️ Installation

### Quick Start (Automated)

1.  **Clone the frequency:**
    ```bash
    git clone https://github.com/yourusername/EventHorizon.git
    cd EventHorizon
    ```

2.  **Run build script:**
    ```bash
    ./build.sh
    ```
    This automatically installs `uv` and all dependencies.

3.  **Initialize Systems:**
    Run the interactive setup script to configure the environment:
    ```bash
    python init_project.py
    ```

4.  **Launch Sequence:**
    ```bash
    uv run python manage.py runserver
    ```

5.  **Access Terminal:**
    Open `http://127.0.0.1:8000` in your browser.

### Manual Installation

1.  **Clone the frequency:**
    ```bash
    git clone https://github.com/yourusername/EventHorizon.git
    cd EventHorizon
    ```

2.  **Install `uv`:**
    ```bash
    # macOS / Linux
    curl -LsSf https://astral.sh/uv/install.sh | sh

    # Windows
    powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
    ```

3.  **Install Dependencies:**
    ```bash
    uv sync
    npm install  # For Tailwind CSS
    npm run build:css
    ```

4.  **Initialize Systems:**
    ```bash
    python init_project.py
    ```

5.  **Launch Sequence:**
    ```bash
    uv run python manage.py runserver
    ```

6.  **Access Terminal:**
    Open `http://127.0.0.1:8000` in your browser.

## ⚙️ Configuration

Event Horizon is configured via environment variables in `.env`:

**Database:** Use `DATABASE_URL` to connect to PostgreSQL or MySQL:
```env
# PostgreSQL
DATABASE_URL=postgresql://user:password@localhost:5432/eventhorizon

# MySQL
DATABASE_URL=mysql://user:password@localhost:3306/eventhorizon
```
Defaults to SQLite if not set. See [Database Configuration](docs/setup/configuration.md#database-configuration) for details.

**Storage:** Configure S3-compatible storage for media files:
```env
STORAGE_BACKEND=s3  # or 'minio', 'local'
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
AWS_STORAGE_BUCKET_NAME=your-bucket
```

For complete configuration options, see [Configuration Guide](docs/setup/configuration.md).

## 🤝 Contributing

Transmission lines are open. Fork the repository and submit a pull request with your enhancements.

## 📄 License

Classified. (MIT License)
