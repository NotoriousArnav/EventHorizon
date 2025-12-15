# Deployment

## Production Checklist

Before deploying to a live environment:

1.  **Set `DEBUG=False`** in your `.env` file.
2.  **Generate a strong `SECRET_KEY`**.
3.  **Configure a Production Database** (PostgreSQL is recommended over SQLite).
4.  **Set `ALLOWED_HOSTS`** to your domain name.
5.  **Use a WSGI Server** like Gunicorn or uWSGI, not `runserver`.

## Using Gunicorn

1.  Install Gunicorn:
    ```bash
    pip install gunicorn
    ```

2.  Run the application:
    ```bash
    gunicorn EventHorizon.wsgi:application --bind 0.0.0.0:8000
    ```

## Docker Deployment (Optional)

A basic `Dockerfile` example:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["gunicorn", "EventHorizon.wsgi:application", "--bind", "0.0.0.0:8000"]
```
