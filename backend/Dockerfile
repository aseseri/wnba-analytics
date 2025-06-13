# backend/Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Run the model building script to generate the .joblib files INSIDE the image
RUN python build_similarity_model.py

# Expose the port the app runs on
EXPOSE 8000

# Note: We are no longer using the [...] format. This is the "shell form".
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
