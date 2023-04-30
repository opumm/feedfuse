from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, HttpUrl


class ItemSchemaBase(BaseModel):
    title: Optional[str]
    url: Optional[HttpUrl]
    guid: Optional[str]
    description: Optional[str] = None
    feed_id: Optional[int]
    published_at: Optional[datetime]

    class Config:
        orm_mode = True


class CreateItemSchema(ItemSchemaBase):
    guid: str
    feed_id: int


class UpdateItemSchema(ItemSchemaBase):
    title: Optional[str] = None
    url: Optional[HttpUrl] = None
    description: Optional[str] = None


class ItemSchema(ItemSchemaBase):
    id: int


class ItemQuerySortEnum(str, Enum):
    published_at = "published_at"


class CommonQueryOrderEnum(str, Enum):
    asc = "asc"
    desc = "desc"


class CommonQueryParamsModel(BaseModel):
    order: CommonQueryOrderEnum | None = CommonQueryOrderEnum.asc
    sort: str | None

    class Config:
        fields = {
            "order": {"exclude": True},
            "sort": {"exclude": True},
        }


class ItemQueryParams(CommonQueryParamsModel):
    feed_id: int | None = None
    is_marked_read: bool | None = None
    sort: ItemQuerySortEnum | None = None
