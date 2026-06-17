#!/usr/bin/env bash
set -e

pip install --upgrade pip
pip install "setuptools<81"
pip install numpy==2.4.6
pip install dlib==19.24.2
pip install face-recognition==1.3.0
pip install git+https://github.com/ageitgey/face_recognition_models.git
pip install opencv-contrib-python-headless==4.10.0.84
pip install mediapipe==0.10.35
pip install -r requirements.txt

python manage.py collectstatic --noinput
python manage.py migrate

python manage.py shell -c "
from django.contrib.auth import get_user_model
import os
User = get_user_model()
username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@visionvote.com')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin123')
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print('Superuser created.')
else:
    print('Superuser already exists.')
"