from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apis.api.system_router import router as system_router
from apis.api.weather_router import router as weather_router
from apis.api.crypto_router import router as crypto_router
from apis.api.command_router import router as command_router

app = FastAPI(title="System Monitor API")

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

app.include_router(system_router, prefix="/api")
app.include_router(weather_router, prefix="/api")
app.include_router(crypto_router, prefix="/api")
app.include_router(command_router, prefix="/api")