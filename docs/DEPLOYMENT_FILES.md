# Deployment Configuration Files - Quick Reference

This document provides a quick overview of all deployment-related files in Event Horizon.

## Files Overview

### Core Deployment Files

| File | Purpose | Used By |
|------|---------|---------|
| `vercel.json` | Vercel serverless deployment configuration | Vercel |
| `Procfile` | Process definitions for web and release commands | Railway, Render, Heroku |
| `gunicorn_config.py` | Gunicorn WSGI server configuration | All traditional servers (VPS, Railway, Render, etc.) |
| `requirements.txt` | Python dependencies for pip-based deployments | Most hosting platforms |
| `runtime.txt` | Python version specification | Heroku, some PaaS platforms |

### Supporting Files

| File | Purpose |
|------|---------|
| `pyproject.toml` | Python project dependencies (uv/pip) |
| `build.sh` | Automated build script for dependencies |
| `init_project.py` | Interactive project setup script |
| `.env.example` | Template for environment variables |

---

## File Details

### vercel.json

**Purpose:** Configure Vercel serverless deployment

**Key Features:**
- Python 3.12 runtime
- Static file serving from `staticfiles/`
- WSGI application configuration
- Sydney region (syd1) for proximity to Supabase
- Automatic static file builds

**When to use:** Deploying to Vercel (experimental - Django has limitations on serverless)

---

### Procfile

**Purpose:** Define process types for PaaS platforms

**Contents:**
```
web: gunicorn EventHorizon.wsgi:application -c gunicorn_config.py
release: python manage.py migrate --noinput && python manage.py collectstatic --noinput
```

**Process Types:**
- `web`: Main web server process (Gunicorn with config)
- `release`: Pre-deployment tasks (migrations, static files)

**When to use:** Railway, Render, Heroku deployments

---

### gunicorn_config.py

**Purpose:** Production-ready Gunicorn WSGI server configuration

**Key Features:**
- Auto-scaling workers based on CPU cores
- Gevent worker class for better concurrency
- PostgreSQL health checks on startup
- Static file verification
- Comprehensive logging configuration
- Environment variable configuration
- Production hooks and lifecycle management

**Configuration Options (via environment variables):**
```bash
PORT=8000                          # Server port (default: 8000)
GUNICORN_WORKERS=4                 # Number of workers (default: 2*CPU+1)
GUNICORN_WORKER_CLASS=gevent       # Worker type (default: gevent)
GUNICORN_TIMEOUT=120               # Request timeout in seconds
GUNICORN_LOG_LEVEL=info            # Log level
GUNICORN_RELOAD=true               # Auto-reload on code changes (dev only)
```

**Usage Examples:**
```bash
# Production
gunicorn EventHorizon.wsgi:application -c gunicorn_config.py

# Development with auto-reload
GUNICORN_RELOAD=true gunicorn EventHorizon.wsgi:application -c gunicorn_config.py

# Custom workers
GUNICORN_WORKERS=8 gunicorn EventHorizon.wsgi:application -c gunicorn_config.py
```

**When to use:** VPS, Railway, Render, any traditional server deployment

---

### requirements.txt

**Purpose:** Python dependencies in pip format

**Generated from:** `pyproject.toml` using `uv pip compile`

**Key Dependencies:**
- Django 6.0
- Gunicorn with gevent workers
- WhiteNoise for static files
- PostgreSQL driver (psycopg2)
- Django REST Framework
- django-allauth for authentication
- django-oauth-toolkit for OAuth2
- django-rest-knox for API tokens
- django-storages with boto3 for S3
- And more...

**Regenerate:**
```bash
uv pip compile pyproject.toml -o requirements.txt
```

**When to use:** Platforms that don't support `pyproject.toml` (most PaaS platforms)

---

### runtime.txt

**Purpose:** Specify Python version for platform detection

**Contents:**
```
python-3.12
```

**When to use:** Heroku, some PaaS platforms that need explicit Python version

---

## Deployment Settings in settings.py

### WhiteNoise Configuration

**Added to MIDDLEWARE:**
```python
"whitenoise.middleware.WhiteNoiseMiddleware",  # After SecurityMiddleware
```

**Storage Backend:**
```python
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}
```

**Benefits:**
- Serves static files efficiently from Django
- Compression (gzip/brotli)
- Far-future cache headers
- No need for separate static file server

---

## Quick Start Commands

### Local Development
```bash
# Install dependencies
uv sync
npm install

# Build assets
npm run build:css

# Run migrations
uv run python manage.py migrate

# Collect static files
uv run python manage.py collectstatic --noinput

# Start development server
uv run python manage.py runserver
# OR with Gunicorn
GUNICORN_RELOAD=true uv run gunicorn EventHorizon.wsgi:application -c gunicorn_config.py
```

### Production VPS
```bash
# After setup (see DEPLOYMENT.md), start with systemd
sudo systemctl start eventhorizon
sudo systemctl status eventhorizon

# Or run directly
uv run gunicorn EventHorizon.wsgi:application -c gunicorn_config.py
```

### Railway/Render/Heroku
```bash
# Push to Git
git push origin main

# Platform auto-deploys using Procfile
# Runs: release process, then web process
```

### Vercel
```bash
# Deploy
vercel --prod

# Or connect GitHub repo for auto-deploys
```

---

## Environment Variables

### Required for All Platforms

```bash
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
DATABASE_URL=postgresql://user:pass@host:5432/db
```

### Optional but Recommended

```bash
# Email
EMAIL_BACKEND=smtp
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Storage
USE_S3_STORAGE=True
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
AWS_STORAGE_BUCKET_NAME=your-bucket
AWS_S3_ENDPOINT_URL=https://your-endpoint

# Security
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

### Gunicorn-Specific (VPS only)

```bash
GUNICORN_WORKERS=4
GUNICORN_WORKER_CLASS=gevent
GUNICORN_TIMEOUT=120
PORT=8000
```

---

## Troubleshooting

### Static files not loading
```bash
# Check if CSS is compiled
ls -lh static/css/output.css

# Rebuild
npm run build:css

# Collect static files
uv run python manage.py collectstatic --noinput --clear
```

### Gunicorn not starting
```bash
# Check configuration
uv run python -c "import gunicorn_config"

# Check database connection
uv run python manage.py dbshell

# Skip startup checks
touch .skip_message
```

### Database connection errors
```bash
# Verify DATABASE_URL
echo $DATABASE_URL

# Test connection
uv run python manage.py migrate --plan
```

---

## Platform-Specific Notes

### Railway
- Uses `Procfile` automatically
- Provides PostgreSQL with `DATABASE_URL`
- Auto-deploys on git push
- Runs `release` command before `web`

### Render
- Uses `Procfile` automatically
- Free PostgreSQL available
- Build command: `./build.sh && python manage.py collectstatic --noinput`
- Start command: `gunicorn EventHorizon.wsgi:application -c gunicorn_config.py`

### Heroku
- Uses `Procfile` and `runtime.txt`
- Requires `requirements.txt`
- Add PostgreSQL: `heroku addons:create heroku-postgresql:mini`

### Vercel
- Uses `vercel.json`
- Serverless functions (cold starts)
- External database required (Supabase, Neon, etc.)
- Limited Django support

### VPS
- Uses `gunicorn_config.py` with systemd
- Full control over environment
- Nginx as reverse proxy
- Manual setup but most flexible

---

## Maintenance Commands

### Update Dependencies
```bash
# Update pyproject.toml, then:
uv sync
uv pip compile pyproject.toml -o requirements.txt
git add pyproject.toml uv.lock requirements.txt
git commit -m "Update dependencies"
```

### Deploy New Version
```bash
# Git-based platforms (Railway, Render, Heroku, Vercel)
git push origin main

# VPS
git pull origin main
uv sync
npm install && npm run build:css
uv run python manage.py migrate
uv run python manage.py collectstatic --noinput
sudo systemctl restart eventhorizon
```

---

## Security Checklist

Before deploying to production:

- [ ] Set `DEBUG=False`
- [ ] Use strong `SECRET_KEY` (50+ characters)
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Enable SSL/HTTPS
- [ ] Set `SECURE_SSL_REDIRECT=True`
- [ ] Set `SESSION_COOKIE_SECURE=True`
- [ ] Set `CSRF_COOKIE_SECURE=True`
- [ ] Use environment variables (never commit secrets)
- [ ] Set up database backups
- [ ] Configure monitoring/error tracking

---

## Additional Resources

- **Full Deployment Guide:** `DEPLOYMENT.md`
- **Development Setup:** `DEVELOPMENT.md`
- **API Documentation:** `docs/api/`
- **Storage Guide:** `docs/storage/`

---

## Support

If you encounter issues:
1. Check `DEPLOYMENT.md` for detailed platform guides
2. Review environment variables in `.env.example`
3. Run `uv run python manage.py check --deploy` for security checks
4. Check platform-specific logs (Railway dashboard, Render logs, etc.)
