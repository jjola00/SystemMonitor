from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import system_router, weather_router, crypto_router

app = FastAPI(title="System Monitor API")

# Update CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080",  # For local development
        "https://jjola00.github.io",  # Your GitHub Pages URL
        "https://my-fastapi-backend-miau.onrender.com",  # Your Render backend URL
    ],
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Include routers
app.include_router(system_router.router, prefix="/api")
app.include_router(weather_router.router, prefix="/api")
app.include_router(crypto_router.router, prefix="/api")