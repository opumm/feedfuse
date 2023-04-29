from typing import List, Optional, Any

from sqlalchemy import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.models import Feed, Subscription
from app.schemas import CreateFeedSchema, UpdateFeedSchema


async def create_feed(session: AsyncSession, feed: CreateFeedSchema) -> Feed:
    db_feed = Feed(**feed.dict())
    session.add(db_feed)
    await session.commit()
    await session.refresh(db_feed)
    return db_feed


async def get_feed(
    session: AsyncSession, feed_id: int, *, load_items: bool = False
) -> Optional[Feed]:
    query = select(Feed).where(Feed.id == feed_id)
    if load_items:
        query = query.options(selectinload(Feed.feed_item))
    result = await session.execute(query)
    return result.scalar_one_or_none()


async def get_feed_by_user(session: AsyncSession, user_id: int) -> List[Optional[Feed]]:
    query = select(Feed).join(Subscription).where(Subscription.user_id == user_id, Subscription.is_active)

    feeds_in_db = await session.execute(query)
    return feeds_in_db.scalars().all()


async def get_feed_by_url(session: AsyncSession, url: str) -> Optional[Feed]:
    query = select(Feed).where(Feed.url == url)
    result = await session.execute(query)
    return result.scalar_one_or_none()


async def get_feeds(
    session: AsyncSession, *, skip: int = 0, limit: int = 100
) -> List[Feed]:
    query = select(Feed).offset(skip).limit(limit)
    result = await session.execute(query)
    return result.scalars().all()


async def update_feed(
    session: AsyncSession, feed_id: int, feed_update: UpdateFeedSchema
) -> Optional[Feed]:
    db_feed = await get_feed(session, feed_id)
    if not db_feed:
        return None
    update_data = feed_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_feed, field, value)
    await session.commit()
    await session.refresh(db_feed)
    return db_feed


async def enable_update(session: AsyncSession, feed_id: int) -> Optional[Feed]:
    db_feed = await get_feed(session, feed_id)
    if not db_feed:
        return None
    if db_feed.is_update_enabled:
        return db_feed

    db_feed.is_update_enabled = True
    await session.commit()
    await session.refresh(db_feed)
    return db_feed
