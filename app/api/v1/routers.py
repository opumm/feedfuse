from fastapi import APIRouter

from app.api.v1.endpoints import feeds, items, login, users

api_router = APIRouter()

api_router.include_router(feeds.router, prefix="/feeds", tags=["Feeds"])
api_router.include_router(items.router, prefix="/items", tags=["Items"])
api_router.include_router(login.router, tags=["Login"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
