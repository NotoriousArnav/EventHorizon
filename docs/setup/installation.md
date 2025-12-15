# Installation Guide

## Prerequisites

- **Python 3.12+**
- **pip** (Python Package Manager)
- **Git**

## Step-by-Step Installation

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/NotoriousArnav/EventHorizon.git
    cd EventHorizon
    ```

2.  **Install Dependencies**
    We use `uv` for fast dependency management, but `pip` works too.
    
    Using `pip`:
    ```bash
    pip install -r requirements.txt
    ```
    
    Using `uv`:
    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    uv sync
    ```

3.  **Environment Setup**
    Create a `.env` file in the root directory:
    ```env
    DEBUG=True
    SECRET_KEY=your-secret-key-here
    ALLOWED_HOSTS=localhost,127.0.0.1
    ```

4.  **Database Migration**
    Initialize the SQLite database:
    ```bash
    python manage.py migrate
    ```

5.  **Create Superuser** (Admin Access)
    ```bash
    python manage.py createsuperuser
    ```

6.  **Run the Server**
    ```bash
    python manage.py runserver
    ```
    Access the site at `http://127.0.0.1:8000/`.

## Troubleshooting

- **ModuleNotFoundError:** Ensure your virtual environment is activated (`source .venv/bin/activate` or `.\.venv\Scripts\activate`).
- **Port 8000 in use:** Run on a different port: `python manage.py runserver 8080`.
