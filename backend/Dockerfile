# backend/Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Note: We are no longer using the [...] format. This is the "shell form".
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
