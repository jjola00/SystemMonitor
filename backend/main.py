from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from api.router import router
from utils.logger import log_info, log_error

app = FastAPI(
    title="System Monitor API",
    description="API for monitoring system and external metrics",
    version="1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the unified router
app.include_router(router, prefix="/api")

# Root Endpoint
@app.get("/")
async def root():
    log_info("Root endpoint accessed")
    return {"message": "System Monitor API is running"}

if __name__ == "__main__":
    log_info("Starting System Monitor API...")
    try:
        uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    except Exception as e:
        log_error(f"Error starting API: {e}")
