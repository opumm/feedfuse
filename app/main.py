from fastapi import FastAPI

from app.api.health import router as health_api_router
from app.api.v1.routers import api_router
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API for aggregating and managing RSS feeds",
    version="0.1.0",
    contact={"name": "Mohammad Mohiuddin", "email": "opummjopu@gmail.com"},
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(health_api_router, tags=["Health"])
