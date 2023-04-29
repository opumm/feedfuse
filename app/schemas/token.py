from typing import Optional

from pydantic import BaseModel


class TokenSchema(BaseModel):
    access_token: str
    token_type: str


class TokenPayloadSchema(BaseModel):
    sub: Optional[int] = None
