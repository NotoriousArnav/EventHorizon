# Event Horizon - Futuristic Event Management Platform
# Copyright (C) 2025-2026 Arnav Ghosh
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

"""
Gunicorn WSGI server configuration for EventHorizon.
For use with traditional server deployments (VPS, Railway, Render, etc.)
"""

from multiprocessing import cpu_count
from os import environ, path
import sys


def check_postgres():
    """
    Check if PostgreSQL database is accessible.
    Only runs if DATABASE_URL is set.
    """
    import os

    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        print("⚠️  No DATABASE_URL found. Using default SQLite for development.")
        return True

    try:
        import psycopg2
        from urllib.parse import urlparse

        result = urlparse(database_url)

        # Extract connection parameters
        conn = psycopg2.connect(
            database=result.path[1:],
            user=result.username,
            password=result.password,
            host=result.hostname,
            port=result.port or 5432,
            connect_timeout=10,
        )
        cursor = conn.cursor()

        # Check if migrations are applied
        cursor.execute("SELECT COUNT(*) FROM django_migrations;")
        result_row = cursor.fetchone()
        count = result_row[0] if result_row else 0

        print(f"✓ Database connected successfully. {count} migrations applied.")
        cursor.close()
        conn.close()
        return True

    except ImportError:
        print("⚠️  psycopg2 not installed. Cannot verify PostgreSQL connection.")
        print("   Install: pip install psycopg2-binary")
        return False
    except Exception as e:
        print(f"❌ Database connection failed: {str(e)}")
        print("   Please check your DATABASE_URL and ensure:")
        print("   1. PostgreSQL is running")
        print("   2. Database exists")
        print("   3. Migrations have been applied (python manage.py migrate)")
        return False


def check_static_files():
    """Check if static files have been collected."""
    static_root = path.join(path.dirname(__file__), "staticfiles")

    if not path.exists(static_root):
        print("⚠️  staticfiles/ directory not found.")
        print("   Run: python manage.py collectstatic --noinput")
        return False

    # Check for CSS
    css_file = path.join(static_root, "css", "output.css")
    if not path.exists(css_file):
        print("⚠️  Tailwind CSS not compiled.")
        print("   Run: npm run build:css")
        print("   Then: python manage.py collectstatic --noinput")
        return False

    print("✓ Static files ready")
    return True


# Run startup checks (can be skipped with .skip_message file)
if not path.exists(".skip_message"):
    db_ok = check_postgres()
    static_ok = check_static_files()

    if not db_ok or not static_ok:
        print("""
╔═══════════════════════════════════════════════════════════════╗
║                   Event Horizon Production                     ║
╚═══════════════════════════════════════════════════════════════╝

Welcome to Event Horizon!

Before starting the server, ensure:
  1. Database migrations are applied:
     $ python manage.py migrate
  
  2. Static files are collected:
     $ python manage.py collectstatic --noinput
  
  3. Tailwind CSS is compiled:
     $ npm run build:css
  
  4. Environment variables are set (.env file):
     - SECRET_KEY
     - DATABASE_URL (for PostgreSQL)
     - ALLOWED_HOSTS
     - EMAIL_* (for production emails)
     - AWS_* (if using S3 for media storage)

To skip this message:
    $ touch .skip_message

Documentation: README.md, DEPLOYMENT.md, docs/
    """)

# ============================================================================
# Gunicorn Configuration
# ============================================================================

# Bind to all interfaces on the specified port
bind = "0.0.0.0:" + environ.get("PORT", "8000")

# Worker processes - auto-scale based on CPU cores
# Rule of thumb: (2 x $num_cores) + 1
workers = int(environ.get("GUNICORN_WORKERS", cpu_count() * 2 + 1))

# Worker class - gevent for better concurrency with Django
# Alternatives: 'sync' (default), 'eventlet', 'tornado'
worker_class = environ.get("GUNICORN_WORKER_CLASS", "gevent")

# Worker connections (only for async workers like gevent)
worker_connections = int(environ.get("GUNICORN_WORKER_CONNECTIONS", 1000))

# Timeout for workers (in seconds)
# Set higher for long-running requests (file uploads, exports)
timeout = int(environ.get("GUNICORN_TIMEOUT", 120))

# Graceful timeout for workers
graceful_timeout = int(environ.get("GUNICORN_GRACEFUL_TIMEOUT", 30))

# Keep-alive timeout
keepalive = int(environ.get("GUNICORN_KEEPALIVE", 5))

# Maximum requests per worker before restart (prevents memory leaks)
max_requests = int(environ.get("GUNICORN_MAX_REQUESTS", 1000))
max_requests_jitter = int(environ.get("GUNICORN_MAX_REQUESTS_JITTER", 50))

# Logging
accesslog = environ.get("GUNICORN_ACCESS_LOG", "-")  # '-' = stdout
errorlog = environ.get("GUNICORN_ERROR_LOG", "-")  # '-' = stderr
loglevel = environ.get(
    "GUNICORN_LOG_LEVEL", "info"
)  # debug, info, warning, error, critical

# Access log format
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Process naming
proc_name = "eventhorizon"

# Server mechanics
daemon = False  # Don't daemonize (container-friendly)
pidfile = None  # No PID file needed for containers

# Development mode (set GUNICORN_RELOAD=true for auto-reload)
reload = environ.get("GUNICORN_RELOAD", "False").lower() in {"true", "1", "yes"}
reload_extra_files = (
    []
    if not reload
    else [
        "EventHorizon/settings.py",
        "static/css/output.css",
    ]
)

# Security
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

# Server socket
backlog = 2048

# SSL (if needed)
# keyfile = environ.get('SSL_KEYFILE', None)
# certfile = environ.get('SSL_CERTFILE', None)

# ============================================================================
# Gunicorn Hooks
# ============================================================================


def on_starting(server):
    """Called just before the master process is initialized."""
    print("🚀 Event Horizon starting...")
    print(f"   Python: {sys.version.split()[0]}")
    print(f"   Workers: {workers} x {worker_class}")


def on_reload(server):
    """Called when gunicorn reloads."""
    print("🔄 Reloading Event Horizon...")


def when_ready(server):
    """Called just after the server is started."""
    print(f"✓ Event Horizon ready at http://{bind}")
    print(f"✓ Environment: {'Development' if reload else 'Production'}")
    if reload:
        print("⚠️  Auto-reload is enabled (development mode)")


def worker_int(worker):
    """Called when a worker receives the SIGINT or SIGQUIT signal."""
    print(f"⚠️  Worker {worker.pid} received interrupt signal")


def worker_abort(worker):
    """Called when a worker receives the SIGABRT signal."""
    print(f"❌ Worker {worker.pid} aborted")


def pre_fork(server, worker):
    """Called just before a worker is forked."""
    pass


def post_fork(server, worker):
    """Called just after a worker has been forked."""
    pass


def pre_exec(server):
    """Called just before a new master process is forked."""
    print("🔄 Forking new master process...")


def pre_request(worker, req):
    """Called just before a worker processes the request."""
    pass


def post_request(worker, req, environ, resp):
    """Called after a worker processes the request."""
    pass


def child_exit(server, worker):
    """Called just after a worker has been exited."""
    pass


def worker_exit(server, worker):
    """Called just after a worker has been exited."""
    pass


def nworkers_changed(server, new_value, old_value):
    """Called just after num_workers has been changed."""
    print(f"📊 Workers changed: {old_value} → {new_value}")


def on_exit(server):
    """Called just before exiting gunicorn."""
    print("👋 Event Horizon shutting down...")


# ============================================================================
# Usage Examples
# ============================================================================
"""
Development (with auto-reload):
    $ GUNICORN_RELOAD=true gunicorn EventHorizon.wsgi:application -c gunicorn_config.py
    $ gunicorn EventHorizon.wsgi:application -c gunicorn_config.py --reload

Production:
    $ gunicorn EventHorizon.wsgi:application -c gunicorn_config.py

Custom workers:
    $ GUNICORN_WORKERS=4 gunicorn EventHorizon.wsgi:application -c gunicorn_config.py

With environment variables:
    $ export GUNICORN_WORKERS=8
    $ export GUNICORN_WORKER_CLASS=gevent
    $ export GUNICORN_TIMEOUT=60
    $ gunicorn EventHorizon.wsgi:application -c gunicorn_config.py

Using specific port:
    $ PORT=3000 gunicorn EventHorizon.wsgi:application -c gunicorn_config.py

Direct command line (bypasses config):
    $ gunicorn EventHorizon.wsgi:application --bind 0.0.0.0:8000 --workers 4

Behind Nginx (production setup):
    $ gunicorn EventHorizon.wsgi:application -c gunicorn_config.py --bind unix:/tmp/eventhorizon.sock

Systemd service example:
    [Unit]
    Description=Event Horizon Gunicorn Service
    After=network.target

    [Service]
    Type=notify
    User=www-data
    Group=www-data
    WorkingDirectory=/var/www/eventhorizon
    Environment="PATH=/var/www/eventhorizon/venv/bin"
    ExecStart=/var/www/eventhorizon/venv/bin/gunicorn EventHorizon.wsgi:application -c gunicorn_config.py
    ExecReload=/bin/kill -s HUP $MAINPID
    KillMode=mixed
    TimeoutStopSec=5
    PrivateTmp=true

    [Install]
    WantedBy=multi-user.target

Docker example:
    CMD ["gunicorn", "EventHorizon.wsgi:application", "-c", "gunicorn_config.py"]
"""
