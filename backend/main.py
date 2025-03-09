#backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.endpoints import router as general_router
from api.device_api import router as device_router
from api.metrics_api import router as metrics_router
import uvicorn

app = FastAPI(title="System Monitor API", description="API for monitoring system and external metrics", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(general_router, prefix="/api")
app.include_router(device_router, prefix="/api/device")
app.include_router(metrics_router, prefix="/api/metrics")

@app.get("/")
def root():
    return {"message": "System Monitor API is running"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)