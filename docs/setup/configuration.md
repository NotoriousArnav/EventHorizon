# Configuration

## Environment Variables

Event Horizon uses `python-dotenv` to manage configuration. Create a `.env` file in the project root.

| Variable | Description | Default | Required |
| :--- | :--- | :--- | :--- |
| `DEBUG` | Enable debug mode (Do not use in production) | `False` | Yes |
| `SECRET_KEY` | Django secret key for cryptographic signing | - | Yes |
| `ALLOWED_HOSTS` | Comma-separated list of valid hostnames | `127.0.0.1` | Yes |
| `DATABASE_URL` | Database connection string (if not using SQLite) | - | No |
| `EMAIL_BACKEND` | Django email backend path | `console` | No |

## Static Files

To serve static files in production, configure your web server (Nginx/Apache) to serve the `staticfiles/` directory after running:

```bash
python manage.py collectstatic
```

## Email Configuration

By default, the system prints emails to the console for development. To configure SMTP for production, add these to your `.env`:

```env
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```
