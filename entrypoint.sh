#!/bin/sh

mkdir -p /app/data

echo ">>> Running migrations..."
python manage.py migrate --noinput

echo ">>> Creating superuser if not exists..."
python manage.py shell << 'PYEOF'
from django.contrib.auth import get_user_model
import os
User = get_user_model()

username = os.environ.get("DJANGO_SUPERUSER_USERNAME", "admin")
email    = os.environ.get("DJANGO_SUPERUSER_EMAIL", "admin@visionvote.com")
password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "admin123")

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f"Superuser '{username}' created.")
else:
    print(f"Superuser '{username}' already exists. Skipping.")
PYEOF

echo ">>> Collecting static files..."
python manage.py collectstatic --noinput

echo ">>> Starting server..."
exec gunicorn VisionVote.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --timeout 300 \
    --workers 2