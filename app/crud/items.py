from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.items import Item
from app.schemas.items import CreateItemSchema, UpdateItemSchema


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
