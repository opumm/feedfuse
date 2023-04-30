from datetime import datetime
from typing import List, Optional

from app import crud
from app.db.session import get_session
from app.schemas.feeds import FeedSchema, UpdateFeedSchema
from app.schemas.items import CreateItemSchema, ItemSchema, UpdateItemSchema


def parse_datetime_string(datetime_str):
    try:
        return datetime.strptime(datetime_str, "%a, %d %b %Y %H:%M:%S %Z")
    except ValueError:
        return datetime.strptime(datetime_str, "%a, %d %b %Y %H:%M:%S %z")


async def fetch_feed() -> List[FeedSchema]:
    async with get_session() as session:
        feeds = await crud.feeds.get_update_enabled_feeds(session)
        feeds = [FeedSchema.from_orm(feed) for feed in feeds]
        return feeds


async def update_feed_in_db(feed_id: int, new_feed: UpdateFeedSchema) -> None:
    async with get_session() as session:
        await crud.feeds.update_feed(session, feed_id, new_feed)


async def pause_feed_update(feed_id: int) -> None:
    async with get_session() as session:
        await crud.feeds.pause_update(session, feed_id)


async def get_item_from_db(item_guid: str) -> Optional[ItemSchema]:
    async with get_session() as session:
        item = await crud.items.get_item_by_guid(session, item_guid)
        if item:
            return ItemSchema.from_orm(item)
        return None


async def update_item_in_db(item_id: int, new_item: UpdateItemSchema) -> None:
    async with get_session() as session:
        await crud.items.update_item(session, item_id, new_item)


async def create_item_in_db(new_item: CreateItemSchema) -> None:
    async with get_session() as session:
        await crud.items.create_item(session, new_item)
