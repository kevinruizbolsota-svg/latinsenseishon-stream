FROM python:3.10-slim

# Instalar dependencias del sistema y FFmpeg completo
RUN apt-get update && apt-get install -y \
    ffmpeg \
    curl \
    git \
    fonts-dejavu-core \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copiar archivos del motor
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Puerto para webhooks de N8N y comprobación de salud
EXPOSE 7860

CMD ["python", "app.py"]
