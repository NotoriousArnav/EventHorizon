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

## 🛠️ Installation

1.  **Clone the frequency:**
    ```bash
    git clone https://github.com/yourusername/EventHorizon.git
    cd EventHorizon
    ```

2.  **Initialize Environment:**
    ```bash
    uv sync
    # OR
    pip install -r requirements.txt
    ```

3.  **Configure Credentials:**
    Create a `.env` file:
    ```env
    DEBUG=True
    SECRET_KEY=your-secret-key
    ```

4.  **Launch Systems:**
    ```bash
    python manage.py migrate
    python manage.py runserver
    ```

5.  **Access Terminal:**
    Open `http://127.0.0.1:8000` in your browser.

## 🤝 Contributing

Transmission lines are open. Fork the repository and submit a pull request with your enhancements.

## 📄 License

Classified. (MIT License)
