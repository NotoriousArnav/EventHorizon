
# Development Setup

## Run Django Server
```bash
uv run python manage.py runserver
```

## Watch Tailwind CSS (in another terminal)
```bash
npm run watch:css
```

This will automatically rebuild CSS when you change templates.

## Production Build
```bash
npm run build:css
python manage.py collectstatic --noinput
```

