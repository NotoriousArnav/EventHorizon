# EventHorizon Production Deployment Guide

This guide covers deploying Event Horizon to various hosting platforms.

## Table of Contents

- [Quick Start](#quick-start)
- [Platform-Specific Guides](#platform-specific-guides)
  - [Railway](#railway-recommended)
  - [Render](#render)
  - [Heroku](#heroku)
  - [Vercel](#vercel-experimental)
  - [VPS/Self-Hosted](#vpsself-hosted)
- [Email Configuration](#email-configuration)
- [Storage Configuration](#storage-configuration)
- [Environment Variables](#environment-variables)
- [Production Checklist](#production-checklist)

---

## Quick Start

Event Horizon includes configuration files for multiple deployment platforms:

- `vercel.json` - Vercel serverless deployment
- `Procfile` - Railway, Render, Heroku
- `gunicorn_config.py` - Traditional server deployments
- `requirements.txt` - Python dependencies (for pip-based platforms)
- `pyproject.toml` - Python dependencies (for uv-based development)
- `runtime.txt` - Python version specification

### Dependencies: uv vs requirements.txt

**Development (Local):**
- Use `uv` and `pyproject.toml`
- Install: `uv sync`
- Faster, more reliable dependency resolution

**Production (Most Platforms):**
- Use `requirements.txt` (auto-generated from `pyproject.toml`)
- Platforms like Vercel, Heroku don't support `uv` yet
- Regenerate after dependency changes: `uv pip compile pyproject.toml -o requirements.txt`

**Exception - VPS/Self-Hosted:**
- Can use `uv` directly: `uv sync && uv run gunicorn ...`
- More flexibility and control

---

## Platform-Specific Guides

### Railway (Recommended)

**Best for:** Simple deployment with PostgreSQL included, automatic HTTPS, reasonable pricing.

#### Setup Steps:

1. **Create Railway Account**
   - Visit https://railway.app
   - Sign up with GitHub

2. **Create New Project**
   ```bash
   # Install Railway CLI (optional)
   npm install -g @railway/cli
   
   # Login
   railway login
   
   # Initialize project
   railway init
   ```

3. **Add PostgreSQL**
   - In Railway dashboard: New → Database → PostgreSQL
   - Railway automatically sets `DATABASE_URL` environment variable

4. **Configure Environment Variables**
   ```bash
   # Required variables (set in Railway dashboard)
   SECRET_KEY=your-secret-key-here
   DEBUG=False
   ALLOWED_HOSTS=your-app.railway.app
   
   # Optional: Email configuration
   EMAIL_BACKEND=smtp
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-app-password
   
   # Optional: S3 Storage (Supabase or AWS)
   AWS_ACCESS_KEY_ID=your-access-key
   AWS_SECRET_ACCESS_KEY=your-secret-key
   AWS_STORAGE_BUCKET_NAME=your-bucket-name
   AWS_S3_ENDPOINT_URL=https://your-project.supabase.co/storage/v1/s3
   ```

5. **Deploy**
   ```bash
   # Push to GitHub
   git push origin main
   
   # Railway auto-deploys from GitHub
   # Or use CLI:
   railway up
   ```

6. **Run Migrations**
   ```bash
   # In Railway dashboard → Variables → Add ONE_OFF_COMMAND
   python manage.py migrate
   python manage.py createsuperuser
   ```

**Pricing:** $5/month free credit, then ~$10-20/month

---

### Render

**Best for:** Free tier with PostgreSQL, easy setup, automatic deployments.

#### Setup Steps:

1. **Create Render Account**
   - Visit https://render.com
   - Sign up with GitHub

2. **Create Web Service**
   - Dashboard → New → Web Service
   - Connect your GitHub repository
   - Configure:
     - **Name:** eventhorizon
     - **Environment:** Python 3
     - **Build Command:** `./build.sh && python manage.py collectstatic --noinput`
     - **Start Command:** `gunicorn EventHorizon.wsgi:application -c gunicorn_config.py`

3. **Add PostgreSQL Database**
   - Dashboard → New → PostgreSQL
   - Copy the Internal Database URL
   - Add to web service environment variables as `DATABASE_URL`

4. **Configure Environment Variables**
   ```bash
   SECRET_KEY=your-secret-key-here
   DEBUG=False
   ALLOWED_HOSTS=your-app.onrender.com
   DATABASE_URL=postgresql://...  # Auto-filled by Render
   PYTHON_VERSION=3.12
   ```

5. **Deploy**
   - Push to GitHub
   - Render auto-deploys on every push to main branch

**Pricing:** Free tier (spins down after inactivity) or $7/month

---

### Heroku

**Best for:** Established platform, extensive documentation, add-ons marketplace.

#### Setup Steps:

1. **Install Heroku CLI**
   ```bash
   # macOS
   brew install heroku/brew/heroku
   
   # Ubuntu/Debian
   curl https://cli-assets.heroku.com/install.sh | sh
   ```

2. **Login and Create App**
   ```bash
   heroku login
   heroku create eventhorizon-app
   ```

3. **Add PostgreSQL**
   ```bash
   heroku addons:create heroku-postgresql:mini
   ```

4. **Configure Environment Variables**
   ```bash
   heroku config:set SECRET_KEY='your-secret-key-here'
   heroku config:set DEBUG=False
   heroku config:set ALLOWED_HOSTS=eventhorizon-app.herokuapp.com
   ```

5. **Deploy**
   ```bash
   git push heroku main
   ```

6. **Run Migrations**
   ```bash
   heroku run python manage.py migrate
   heroku run python manage.py createsuperuser
   ```

**Pricing:** ~$5-7/month for Eco dynos + Mini Postgres

---

### Vercel (Experimental)

**Best for:** Developers already using Vercel, serverless architecture.

**⚠️ Warning:** Django on Vercel has limitations:
- Cold starts can be slow
- No WebSockets support
- Limited background task support
- Better alternatives exist for Django (Railway, Render)

**📝 Note on Dependencies:**
- Vercel uses `requirements.txt` (not `pyproject.toml` or `uv`)
- The included `requirements.txt` is auto-generated from `pyproject.toml`
- If you update dependencies, regenerate: `uv pip compile pyproject.toml -o requirements.txt`

#### Setup Steps:

1. **Install Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **Configure `vercel.json`** (already included)
   - Points to `EventHorizon/wsgi.py`
   - Configures static file serving
   - Sets Python 3.12 runtime
   - Uses `requirements.txt` for dependencies

3. **Set Environment Variables**
   ```bash
   vercel env add SECRET_KEY
   vercel env add DATABASE_URL
   vercel env add ALLOWED_HOSTS
   ```

4. **Deploy**
   ```bash
   vercel --prod
   ```

**Note:** You'll need external PostgreSQL (Supabase, Neon, etc.)

**Pricing:** Free hobby tier, then ~$20/month

---

### VPS/Self-Hosted

**Best for:** Full control, cost-effective at scale, learning deployment.

**Platforms:** DigitalOcean, Linode, Vultr, AWS EC2, Azure VM, etc.

#### Setup Steps:

1. **Server Setup** (Ubuntu 22.04 example)
   ```bash
   # Update system
   sudo apt update && sudo apt upgrade -y
   
   # Install Python 3.12
   sudo apt install software-properties-common -y
   sudo add-apt-repository ppa:deadsnakes/ppa -y
   sudo apt install python3.12 python3.12-venv python3-pip -y
   
   # Install PostgreSQL
   sudo apt install postgresql postgresql-contrib -y
   
   # Install Nginx
   sudo apt install nginx -y
   
   # Install Node.js (for Tailwind CSS)
   curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
   sudo apt install nodejs -y
   ```

2. **Database Setup**
   ```bash
   sudo -u postgres psql
   CREATE DATABASE eventhorizon;
   CREATE USER eventhorizon WITH PASSWORD 'secure-password';
   GRANT ALL PRIVILEGES ON DATABASE eventhorizon TO eventhorizon;
   \q
   ```

3. **Application Setup**
   ```bash
   # Create application user
   sudo useradd -m -s /bin/bash eventhorizon
   sudo su - eventhorizon
   
   # Clone repository
   git clone https://github.com/yourusername/EventHorizon.git
   cd EventHorizon
   
   # Install uv
   curl -LsSf https://astral.sh/uv/install.sh | sh
   export PATH="$HOME/.cargo/bin:$PATH"
   
   # Install dependencies
   uv sync
   npm install
   
   # Build assets
   npm run build:css
   
   # Configure .env
   cp .env.example .env
   nano .env  # Edit with your settings
   
   # Run migrations
   uv run python manage.py migrate
   uv run python manage.py collectstatic --noinput
   uv run python manage.py createsuperuser
   ```

4. **Gunicorn Setup**
   ```bash
   # Test gunicorn
   uv run gunicorn EventHorizon.wsgi:application -c gunicorn_config.py
   
   # Create systemd service
   sudo nano /etc/systemd/system/eventhorizon.service
   ```
   
   Add:
   ```ini
   [Unit]
   Description=Event Horizon Gunicorn Service
   After=network.target
   
   [Service]
   Type=notify
   User=eventhorizon
   Group=eventhorizon
   WorkingDirectory=/home/eventhorizon/EventHorizon
   Environment="PATH=/home/eventhorizon/.cargo/bin:/usr/bin"
   ExecStart=/home/eventhorizon/.cargo/bin/uv run gunicorn EventHorizon.wsgi:application -c gunicorn_config.py
   ExecReload=/bin/kill -s HUP $MAINPID
   KillMode=mixed
   TimeoutStopSec=5
   PrivateTmp=true
   Restart=always
   
   [Install]
   WantedBy=multi-user.target
   ```
   
   ```bash
   # Enable and start service
   sudo systemctl enable eventhorizon
   sudo systemctl start eventhorizon
   sudo systemctl status eventhorizon
   ```

5. **Nginx Configuration**
   ```bash
   sudo nano /etc/nginx/sites-available/eventhorizon
   ```
   
   Add:
   ```nginx
   upstream eventhorizon {
       server 127.0.0.1:8000;
   }
   
   server {
       listen 80;
       server_name your-domain.com www.your-domain.com;
       
       client_max_body_size 10M;
       
       location /static/ {
           alias /home/eventhorizon/EventHorizon/staticfiles/;
           expires 30d;
           add_header Cache-Control "public, immutable";
       }
       
       location /media/ {
           alias /home/eventhorizon/EventHorizon/media/;
           expires 30d;
       }
       
       location / {
           proxy_pass http://eventhorizon;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```
   
   ```bash
   # Enable site
   sudo ln -s /etc/nginx/sites-available/eventhorizon /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

6. **SSL with Let's Encrypt**
   ```bash
   sudo apt install certbot python3-certbot-nginx -y
   sudo certbot --nginx -d your-domain.com -d www.your-domain.com
   ```

**Pricing:** $5-10/month for VPS

---

## Email Configuration

EventHorizon supports multiple email backends for production. Choose based on your needs:

### Option 1: SMTP (Gmail, AWS SES, Custom Server)

**Best for:** Small to medium deployments, existing email infrastructure

```bash
# .env configuration
EMAIL_BACKEND=smtp
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@yourdomain.com
```

**Gmail Setup:**
1. Enable 2FA on your Google account
2. Generate App Password: https://myaccount.google.com/apppasswords
3. Use the 16-character password as `EMAIL_HOST_PASSWORD`

**AWS SES Setup:**
```bash
EMAIL_HOST=email-smtp.us-east-1.amazonaws.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-ses-smtp-username
EMAIL_HOST_PASSWORD=your-ses-smtp-password
```

### Option 2: SendGrid

**Best for:** High-volume transactional emails, detailed analytics

```bash
# Install package
uv add sendgrid-django

# .env configuration
EMAIL_BACKEND=sendgrid
SENDGRID_API_KEY=SG.your-api-key-here
DEFAULT_FROM_EMAIL=noreply@yourdomain.com
```

### Option 3: Mailgun

**Best for:** Developer-friendly API, EU hosting options

```bash
# Install package
uv add django-anymail

# .env configuration
EMAIL_BACKEND=mailgun
MAILGUN_API_KEY=your-mailgun-api-key
MAILGUN_SENDER_DOMAIN=mg.yourdomain.com
DEFAULT_FROM_EMAIL=noreply@yourdomain.com
```

---

## Storage Configuration

Event Horizon uses S3-compatible storage for media files (avatars, etc.)

### Option 1: Supabase Storage (Recommended)

```bash
# .env configuration
USE_S3_STORAGE=True
AWS_ACCESS_KEY_ID=your-supabase-access-key
AWS_SECRET_ACCESS_KEY=your-supabase-secret-key
AWS_STORAGE_BUCKET_NAME=eventhorizon
AWS_S3_ENDPOINT_URL=https://your-project.supabase.co/storage/v1/s3
AWS_S3_REGION_NAME=ap-southeast-2
```

### Option 2: AWS S3

```bash
USE_S3_STORAGE=True
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
AWS_STORAGE_BUCKET_NAME=your-bucket-name
AWS_S3_REGION_NAME=us-east-1
```

### Option 3: Local Storage

```bash
# .env configuration
USE_S3_STORAGE=False
# Media files stored in /media directory
```

---

## Environment Variables

### Required Variables

```bash
# Django Core
SECRET_KEY=your-secret-key-here  # Generate: python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com

# Database
DATABASE_URL=postgresql://user:password@host:5432/database
```

### Optional Variables

```bash
# Email
EMAIL_BACKEND=smtp
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@yourdomain.com

# Storage (S3)
USE_S3_STORAGE=True
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_STORAGE_BUCKET_NAME=your-bucket
AWS_S3_ENDPOINT_URL=https://your-endpoint
AWS_S3_REGION_NAME=us-east-1

# CORS (for API access)
CORS_ALLOW_ALL_ORIGINS=False
CORS_ALLOWED_ORIGINS=https://yourapp.com,https://api.yourapp.com

# Security (recommended for production)
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_BROWSER_XSS_FILTER=True
SECURE_CONTENT_TYPE_NOSNIFF=True

# Gunicorn (for VPS deployments)
GUNICORN_WORKERS=4
GUNICORN_WORKER_CLASS=gevent
GUNICORN_TIMEOUT=120
```

---

## Production Checklist

### Pre-Deployment

- [ ] Set `DEBUG=False`
- [ ] Set strong `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Set up PostgreSQL database
- [ ] Configure email backend
- [ ] Set up S3 storage (optional)
- [ ] Build Tailwind CSS: `npm run build:css`
- [ ] Collect static files: `python manage.py collectstatic --noinput`
- [ ] Run migrations: `python manage.py migrate`

### Security

- [ ] Enable HTTPS/SSL
- [ ] Set `SECURE_SSL_REDIRECT=True`
- [ ] Set `SESSION_COOKIE_SECURE=True`
- [ ] Set `CSRF_COOKIE_SECURE=True`
- [ ] Configure CORS if using APIs
- [ ] Review `ALLOWED_HOSTS`
- [ ] Rotate `SECRET_KEY` regularly

### Email

- [ ] Set `EMAIL_BACKEND` to smtp/sendgrid/mailgun
- [ ] Configure email credentials securely
- [ ] Set `DEFAULT_FROM_EMAIL` to your domain
- [ ] Test email sending: `python manage.py sendtestemail your-email@example.com`
- [ ] Configure DNS records (SPF, DKIM, DMARC)

### Monitoring

- [ ] Set up error logging (Sentry, Rollbar, etc.)
- [ ] Monitor server resources (CPU, memory, disk)
- [ ] Set up uptime monitoring
- [ ] Monitor database performance
- [ ] Track email delivery rates

### Backup

- [ ] Set up automated database backups
- [ ] Back up media files (S3 versioning)
- [ ] Document recovery procedures
- [ ] Test restore process

---

## Testing Deployment

```bash
# Check Django configuration
python manage.py check --deploy

# Test database connection
python manage.py dbshell

# Test email
python manage.py sendtestemail your-email@example.com

# Test static files
python manage.py collectstatic --dry-run

# Run migrations
python manage.py migrate --plan
```

---

## Common Issues

### Static files not loading
```bash
# Rebuild CSS
npm run build:css

# Collect static files
python manage.py collectstatic --noinput --clear

# Check STATIC_ROOT and STATIC_URL in settings
```

### Database connection errors
```bash
# Verify DATABASE_URL format
postgresql://username:password@host:port/database

# Test connection
python manage.py dbshell
```

### Email not sending
```bash
# Test email configuration
python manage.py shell
>>> from django.core.mail import send_mail
>>> send_mail('Test', 'Message', 'from@example.com', ['to@example.com'])
```

---

## Support

- **Documentation:** `docs/` directory
- **GitHub Issues:** https://github.com/yourusername/EventHorizon/issues
- **Development Guide:** `DEVELOPMENT.md`

---

## Platform Comparison

| Platform | Difficulty | Cost | Pros | Cons |
|----------|-----------|------|------|------|
| Railway | ⭐ Easy | $10-20/mo | Simple, PostgreSQL included, auto-deploy | Limited free tier |
| Render | ⭐ Easy | Free/$7/mo | Free tier, simple setup | Free tier sleeps |
| Heroku | ⭐⭐ Medium | $5-15/mo | Mature platform, add-ons | More expensive |
| Vercel | ⭐⭐⭐ Hard | Free/$20/mo | Great for frontend | Not ideal for Django |
| VPS | ⭐⭐⭐⭐ Expert | $5-10/mo | Full control, cheapest | Manual setup, maintenance |

**Recommendation:** Start with Railway or Render for simplicity. Move to VPS when you need more control or have higher traffic.
