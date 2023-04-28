from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class TokenSchema(BaseModel):
    access_token: str
    token_type: str


@router.post("/login", response_model=TokenSchema)
async def login_access_token() -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """

    return {
        "access_token": "super-token",
        "token_type": "bearer",
    }


@router.post("/refresh", response_model=TokenSchema)
async def refresh_token() -> Any:
    """
    Refresh access token
    """

    return {
        "access_token": "super-token",
        "token_type": "bearer",
    }
