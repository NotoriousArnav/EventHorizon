# Configuration

## Environment Variables

Event Horizon uses `python-dotenv` to manage configuration. Create a `.env` file in the project root.

| Variable | Description | Default | Required |
| :--- | :--- | :--- | :--- |
| `DEBUG` | Enable debug mode (Do not use in production) | `False` | Yes |
| `SECRET_KEY` | Django secret key for cryptographic signing | - | Yes |
| `ALLOWED_HOSTS` | Comma-separated list of valid hostnames | `127.0.0.1` | Yes |
| `DATABASE_URL` | Database connection string (see below) | SQLite | No |
| `EMAIL_BACKEND` | Django email backend path | `console` | No |

## Database Configuration

Event Horizon supports multiple database backends through the `DATABASE_URL` environment variable. If not set, it defaults to SQLite.

### Connection String Format

```
<engine>://<user>:<password>@<host>:<port>/<database>
```

### SQLite (Default)

SQLite is used by default for development. No configuration needed, or explicitly set:

```env
# Not needed - this is the default
DATABASE_URL=sqlite:///db.sqlite3
```

### PostgreSQL

For PostgreSQL, install the driver first:

```bash
uv add psycopg2-binary
```

Then configure the connection:

```env
# Basic connection
DATABASE_URL=postgresql://username:password@localhost:5432/eventhorizon

# With SSL (production)
DATABASE_URL=postgresql://username:password@db.example.com:5432/eventhorizon?sslmode=require

# Alternative format (both work)
DATABASE_URL=postgres://username:password@localhost:5432/eventhorizon
```

### MySQL/MariaDB

For MySQL or MariaDB, install the driver:

```bash
uv add mysqlclient
```

Then configure:

```env
DATABASE_URL=mysql://username:password@localhost:3306/eventhorizon
```

### Cloud Database Services

**Heroku Postgres:**
```env
DATABASE_URL=postgres://user:pass@ec2-host.compute-1.amazonaws.com:5432/dbname
```

**DigitalOcean Managed Database:**
```env
DATABASE_URL=postgresql://user:pass@db-postgresql-nyc3-12345.ondigitalocean.com:25060/dbname?sslmode=require
```

**Amazon RDS:**
```env
DATABASE_URL=postgresql://user:pass@mydb.123456.us-east-1.rds.amazonaws.com:5432/eventhorizon
```

### Connection Pooling

The `DATABASE_URL` configuration automatically enables:
- **Connection pooling** (`conn_max_age=600` seconds)
- **Health checks** (`conn_health_checks=True`)

This improves performance by reusing database connections.

### Migration

After changing your database configuration, run migrations:

```bash
python manage.py migrate
```

## Static Files

To serve static files in production, configure your web server (Nginx/Apache) to serve the `staticfiles/` directory after running:

```bash
python manage.py collectstatic
```

## Security Settings

Event Horizon automatically applies production-grade security settings when `DEBUG=False`. These settings protect your application from common security vulnerabilities.

### Automatic Security Features (Production Only)

When `DEBUG=False`, the following security features are automatically enabled:

**HTTPS/SSL:**
- `SECURE_SSL_REDIRECT=True` - Redirects all HTTP traffic to HTTPS
- `SECURE_HSTS_SECONDS=31536000` - Enforces HTTPS for 1 year (configurable)
- `SECURE_HSTS_INCLUDE_SUBDOMAINS=True` - Applies HSTS to subdomains
- `SECURE_HSTS_PRELOAD=True` - Enables HSTS preloading

**Cookie Security:**
- `SESSION_COOKIE_SECURE=True` - Session cookies only sent over HTTPS
- `CSRF_COOKIE_SECURE=True` - CSRF cookies only sent over HTTPS

**Additional Headers:**
- `SECURE_CONTENT_TYPE_NOSNIFF=True` - Prevents MIME type sniffing
- `SECURE_BROWSER_XSS_FILTER=True` - Enables browser XSS protection
- `X_FRAME_OPTIONS=DENY` - Prevents clickjacking attacks

### Customizing Security Settings

You can customize security settings via environment variables:

```env
# Disable SSL redirect (if using a reverse proxy that handles SSL)
SECURE_SSL_REDIRECT=False

# Customize HSTS duration (in seconds)
SECURE_HSTS_SECONDS=2592000  # 30 days

# Disable HSTS on subdomains
SECURE_HSTS_INCLUDE_SUBDOMAINS=False
```

### Development Mode

When `DEBUG=True` (development), all HTTPS/SSL requirements are disabled to allow local testing without SSL certificates.

### Important Notes

**Before Enabling HSTS:**
- Ensure your entire site works correctly over HTTPS
- HSTS cannot be easily undone once enabled
- Start with a short duration (e.g., 300 seconds) for testing
- Read Django's HSTS documentation before production deployment

**For Load Balancers/Reverse Proxies:**
If you're using a load balancer (AWS ELB, Nginx, Cloudflare) that handles SSL termination, you may need to:
- Set `SECURE_SSL_REDIRECT=False` (let the proxy handle redirects)
- Configure `SECURE_PROXY_SSL_HEADER` if needed

## Email Configuration

By default, the system prints emails to the console for development. To configure SMTP for production, add these to your `.env`:

```env
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```
