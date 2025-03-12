from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.api import system_router, weather_router, crypto_router, command_router

app = FastAPI(title="System Monitor API")

# Update CORS settings for cloud deployment
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",                
        "https://jjola00.github.io",           
        "https://my-fastapi-backend-miau.onrender.com", 
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(system_router.router, prefix="/api")
app.include_router(weather_router.router, prefix="/api")
app.include_router(crypto_router.router, prefix="/api")
app.include_router(command_router.router, prefix="/api")