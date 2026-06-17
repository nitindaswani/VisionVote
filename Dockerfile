FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    libportaudio2 \
    libglib2.0-0 \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install "setuptools<81"

# Install heavy packages one by one with no-cache to save memory
RUN pip install --no-cache-dir numpy==2.4.6
RUN pip install --no-cache-dir dlib==19.24.6
RUN pip install --no-cache-dir face-recognition==1.3.0
RUN pip install --no-cache-dir git+https://github.com/ageitgey/face_recognition_models.git
RUN pip install --no-cache-dir opencv-contrib-python-headless==4.10.0.84
RUN pip install --no-cache-dir mediapipe==0.10.35
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]