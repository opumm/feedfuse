import logging
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import coalesce

from app.models.items import Item
from app.models.read_status import ReadStatus
from app.models.subscription import Subscription
from app.schemas.items import CreateItemSchema, ItemQueryParams, UpdateItemSchema


async def create_item(session: AsyncSession, item: CreateItemSchema) -> Item:
    db_item = Item(**item.dict())
    session.add(db_item)
    await session.commit()
    await session.refresh(db_item)
    return db_item


async def get_item(session: AsyncSession, item_id: int) -> Optional[Item]:
    query = select(Item).where(Item.id == item_id)
    result = await session.execute(query)
    return result.scalar_one_or_none()


async def get_items(
    session: AsyncSession, user_id: int, query_params: ItemQueryParams
) -> Optional[Item]:
    if query_params.feed_id:
        subscribed_feed_stmt = (
            select(Subscription.feed_id)
            .where(
                Subscription.user_id == user_id,
                Subscription.is_active,
                Subscription.feed_id == query_params.feed_id,
            )
            .subquery()
        )
    else:
        subscribed_feed_stmt = (
            select(Subscription.feed_id)
            .where(Subscription.user_id == user_id, Subscription.is_active)
            .subquery()
        )

    query = select(Item).where(Item.feed_id == subscribed_feed_stmt.c.feed_id)

    if query_params.status:
        read_item_stmt = (
            select(ReadStatus.item_id).where(ReadStatus.user_id == user_id, ReadStatus.is_read)
        )
        sub_read_item_stmt = read_item_stmt.subquery()
        if query_params.status == 'read':
            query = query.filter(Item.id == sub_read_item_stmt.c.item_id)

        if query_params.status == 'unread':
            result = await session.execute(read_item_stmt)
            read_items = result.scalars().all()
            if len(read_items):
                query = query.filter(Item.id != sub_read_item_stmt.c.item_id)

    if query_params.order == "asc":
        query = query.order_by(Item.updated_at.asc())
    else:
        query = query.order_by(Item.updated_at.desc())

    result = await session.execute(query)
    return result.scalars().all()


async def get_item_by_guid(session: AsyncSession, guid: str) -> Optional[Item]:
    query = select(Item).where(Item.guid == guid)
    result = await session.execute(query)
    return result.scalar_one_or_none()


async def update_item(
    session: AsyncSession, item_id: int, item: UpdateItemSchema
) -> Optional[Item]:
    db_item = await get_item(session=session, item_id=item_id)
    if not db_item:
        return None
    for field, value in item:
        if value:
            setattr(db_item, field, value)
    await session.commit()
    await session.refresh(db_item)
    return db_item


async def delete_item(session: AsyncSession, item_id: int) -> Optional[Item]:
    db_item = await get_item(session=session, item_id=item_id)
    if not db_item:
        return None
    session.delete(db_item)
    await session.commit()
    return db_item


async def get_items_by_feed(session: AsyncSession, feed_id: int) -> List[Item]:
    query = select(Item).where(Item.feed_id == feed_id)
    result = await session.execute(query)
    return result.scalars().all()
