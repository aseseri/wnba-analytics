# backend/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Create a FastAPI instance
app = FastAPI()

# Define allowed origins for cross-origin resource sharing (CORS)
origins = [
    "http://localhost:3000",  # Allows requests from your frontend during development
]

# Apply the CORS middleware to enable communication between frontend and backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # List of allowed origins
    allow_credentials=True,  # Allows cookies to be included in requests
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Define a simple route to test the API
@app.get("/api")
def read_root():
    return {"message": "Hello from the FastAPI Backend!"}
