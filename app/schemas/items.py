from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, HttpUrl

from app.schemas.common_query_params import CommonQueryOrderEnum


class ItemSchemaBase(BaseModel):
    title: Optional[str]
    url: Optional[HttpUrl]
    guid: Optional[str]
    description: Optional[str] = None
    feed_id: Optional[int]
    published_at: Optional[datetime]


class ItemSchema(ItemSchemaBase):
    id: int
    updated_at: datetime

    class Config:
        orm_mode = True


class CreateItemSchema(ItemSchemaBase):
    guid: str
    feed_id: int


class UpdateItemSchema(ItemSchemaBase):
    title: Optional[str] = None
    url: Optional[HttpUrl] = None
    description: Optional[str] = None


class ItemQuerySortEnum(str, Enum):
    updated_at = "updated_at"


class ItemQueryReadStatusEnum(str, Enum):
    read: str = "read"
    unread: str = "unread"


class ItemQueryParams(BaseModel):
    feed_id: Optional[int]
    status: Optional[ItemQueryReadStatusEnum]
    sort: Optional[ItemQuerySortEnum] = ItemQuerySortEnum.updated_at
    order: Optional[CommonQueryOrderEnum] = CommonQueryOrderEnum.desc

    class Config:
        fields = {
            "order": {"exclude": True},
            "sort": {"exclude": True},
        }
