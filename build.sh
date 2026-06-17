#!/usr/bin/env bash

pip install "setuptools<81"
pip install git+https://github.com/ageitgey/face_recognition_models.git
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@visionvote.com', 'admin123')
    print('Superuser created.')
"