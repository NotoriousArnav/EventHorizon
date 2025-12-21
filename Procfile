# Procfile for Railway, Render, Heroku deployments
# https://devcenter.heroku.com/articles/procfile

# Web process: Run Gunicorn with configuration
web: gunicorn EventHorizon.wsgi:application -c gunicorn_config.py

# Release phase: Run migrations and collect static files
# This runs before the web process starts (on Heroku/Railway/Render)
release: python manage.py migrate --noinput && python manage.py collectstatic --noinput
