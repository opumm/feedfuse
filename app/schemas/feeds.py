from datetime import datetime
from typing import Optional

from pydantic import BaseModel, HttpUrl


class FeedSchemaBase(BaseModel):
    url: Optional[HttpUrl] = None


class CreateFeedSchema(FeedSchemaBase):
    url: HttpUrl


class FeedSchema(FeedSchemaBase):
    id: int
    title: Optional[str] = None
    description: Optional[str] = None
    last_built_at: datetime = None
    is_update_enabled: bool
    created_at: datetime

    class Config:
        orm_mode = True


class FeedQueryParams(BaseModel):
    is_update_enabled: Optional[bool] = True
