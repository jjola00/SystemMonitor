# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import system_router, weather_router, crypto_router

app = FastAPI(title="System Monitor API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"], 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)

app.include_router(system_router.router, prefix="/api")
app.include_router(weather_router.router, prefix="/api")
app.include_router(crypto_router.router, prefix="/api")