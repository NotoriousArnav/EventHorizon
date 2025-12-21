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

Transmission lines are open! We welcome contributions from the community.

**Before contributing, please:**
- Read our [Contributing Guide](CONTRIBUTING.md) for detailed guidelines
- Review our code style and testing requirements
- Understand that all contributions will be licensed under GPL-3.0

**Quick start for contributors:**
```bash
# Fork and clone the repository
git clone https://github.com/YOUR-USERNAME/EventHorizon.git

# Set up development environment
./build.sh
python init_project.py

# Create a feature branch
git checkout -b feature/your-feature-name

# Make changes, test, and submit a PR
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for the complete contribution process.

## 📄 License

Event Horizon is **free and open source software** licensed under the [GNU General Public License v3.0 (GPL-3.0)](LICENSE).

### What This Means

**You are free to:**
- **Use** the software for any purpose
- **Study** how the program works and modify it
- **Share** copies of the software
- **Distribute** your modified versions

**Under these conditions:**
- **Source code availability:** If you distribute the software, you must make the source code available
- **Same license:** Derivative works must be licensed under GPL-3.0
- **State changes:** You must document modifications you make
- **No warranty:** The software is provided "as is" without warranty

### Key Points

- **Copyleft:** GPL-3.0 is a "copyleft" license, ensuring the software and its derivatives remain free
- **Commercial use:** You can use Event Horizon commercially, but must comply with GPL-3.0 terms
- **Dependencies:** All dependencies are GPL-3.0 compatible (see [DEPENDENCIES.md](DEPENDENCIES.md))
- **Contributing:** By contributing, you agree to license your contributions under GPL-3.0

### License Files

- **[LICENSE](LICENSE)** - Full GPL-3.0 license text
- **[DEPENDENCIES.md](DEPENDENCIES.md)** - Third-party dependency licenses
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Contributor license agreement

For more information about GPL-3.0, visit:
- [Official GPL-3.0 Text](https://www.gnu.org/licenses/gpl-3.0.html)
- [GPL-3.0 FAQ](https://www.gnu.org/licenses/gpl-faq.html)
- [Quick Guide to GPL-3.0](https://www.gnu.org/licenses/quick-guide-gplv3.html)
