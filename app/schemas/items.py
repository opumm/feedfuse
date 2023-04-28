from datetime import datetime
from enum import Enum

from pydantic import BaseModel, HttpUrl


class ItemSchemaBase(BaseModel):
    title: str
    url: HttpUrl
    guid: str
    description: str | None = None
    feed_id: int
    published_at: datetime

    class Config:
        orm_mode = True


class CreateItemSchema(ItemSchemaBase):
    pass


class UpdateItemSchema(ItemSchemaBase):
    pass


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
