# Development Guide

## Quick Start

### Option 1: Build Script (Fastest)

For a completely automated setup:

```bash
# Install uv and all dependencies automatically
./build.sh

# Then configure your environment
python init_project.py
```

The `build.sh` script will:
- ✓ Install uv package manager (if not present)
- ✓ Install Python dependencies
- ✓ Install Node.js dependencies (if Node.js is available)
- ✓ Build Tailwind CSS
- ✓ Verify installation

### Option 2: Interactive Setup (Recommended)

Run the interactive initialization script to set up everything automatically:

```bash
python init_project.py
```

This will guide you through:
- ✓ Installing dependencies (via uv or pip)
- ✓ Creating .env configuration file
- ✓ Setting up database (SQLite, PostgreSQL, or MySQL)
- ✓ Configuring email backend (Console, SMTP, SendGrid, Mailgun)
- ✓ Setting up storage (Local, S3, MinIO, DigitalOcean, Cloudflare R2)
- ✓ Installing Node.js dependencies
- ✓ Building Tailwind CSS
- ✓ Running database migrations
- ✓ Creating superuser account

### Option 3: Manual Setup

If you prefer manual setup:

1. **Install Dependencies:**
   ```bash
   # Using uv (recommended)
   uv sync
   
   # Or using pip
   pip install -e .
   ```

2. **Create .env file:**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Install Node.js dependencies:**
   ```bash
   npm install
   ```

4. **Build Tailwind CSS:**
   ```bash
   npm run build:css
   ```

5. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

6. **Create superuser:**
   ```bash
   python manage.py createsuperuser
   ```

## Development Workflow

### Run Django Server
```bash
uv run python manage.py runserver
# Or if not using uv:
python manage.py runserver
```

Access at: http://127.0.0.1:8000

### Watch Tailwind CSS (in another terminal)
```bash
npm run watch:css
```

This automatically rebuilds CSS when you change templates or Tailwind configuration.

### Development Tips

**Hot Reloading:**
- Django auto-reloads when Python files change
- Tailwind watch mode auto-rebuilds CSS when templates change
- Run both in separate terminals for best experience

**Database Changes:**
```bash
# Create migration after model changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Check for issues
python manage.py check
```

**Testing:**
```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test events
python manage.py test users

# Run with coverage
coverage run manage.py test
coverage report
```

**Shell Access:**
```bash
# Django shell
python manage.py shell

# Database shell
python manage.py dbshell
```

## Configuration Files

### .env
Environment-specific configuration. Never commit this file!
- Django settings (SECRET_KEY, DEBUG, ALLOWED_HOSTS)
- Database connection (DATABASE_URL)
- Email configuration
- Storage backend settings
- CORS settings

### pyproject.toml
Python dependencies managed by uv or pip.

### package.json
Node.js dependencies for Tailwind CSS build system.

### tailwind.config.js
Tailwind CSS configuration, theme customization, and content paths.

## Production Build
```bash
# Build optimized CSS
npm run build:css

# Collect static files
python manage.py collectstatic --noinput

# Check deployment readiness
python manage.py check --deploy
```

## Common Issues

### Database Connection Errors
Check your DATABASE_URL in .env and ensure:
- Database server is running
- Credentials are correct
- Database exists
- Required driver is installed (psycopg2-binary for PostgreSQL, mysqlclient for MySQL)

### CSS Not Loading
Run:
```bash
npm run build:css
python manage.py collectstatic
```

### Import Errors
Ensure dependencies are installed:
```bash
uv sync
# or
pip install -e .
```

### Permission Errors
Make scripts executable:
```bash
chmod +x init_project.py
chmod +x create_superuser.py
```
