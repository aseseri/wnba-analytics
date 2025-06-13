# backend/Dockerfile

# --- Stage 1: The "base" stage ---
FROM python:3.11-slim AS base
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --- Stage 2: The "development" stage ---
FROM base AS development
WORKDIR /app
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# --- Stage 3: The "production" stage ---
FROM base AS production
WORKDIR /app
COPY . .
RUN python build_similarity_model.py
EXPOSE 8000
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}