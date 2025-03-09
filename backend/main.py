from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from contextlib import asynccontextmanager
from api.router import router
from services.metrics_service import store_local_metrics, store_external_metrics
from utils.logger import log_info

async def collect_and_store_metrics():
    """Runs background metric collection."""
    while True:
        try:
            store_local_metrics()
            store_external_metrics()
            log_info("Metrics collected.")
        except Exception as e:
            log_info(f"Error: {e}")
        await asyncio.sleep(5)

@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(collect_and_store_metrics())
    yield
    task.cancel()

app = FastAPI(title="System Monitor API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"], 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)

app.include_router(router, prefix="/api")
