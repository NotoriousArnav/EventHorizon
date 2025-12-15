import os
import django
from django.contrib.auth import get_user_model

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "EventHorizon.settings")
django.setup()

User = get_user_model()
username = "admin"
email = "admin@eventhorizon.local"
password = "Ihapwics123$"
first_name = "Administrator"
last_name = "Staff"

if not User.objects.filter(username=username).exists():
    print(f"Creating superuser {username}...")
    User.objects.create_superuser(
        username=username,
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
    )
    print(f"Superuser `{username}` with password `{password}` created.")
else:
    print(f"Superuser {username} already exists.")
