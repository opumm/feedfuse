from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.read_status import ReadStatus


async def create_read_status(
    session: AsyncSession, item_id: int, user_id: int, is_read: bool
) -> Optional[ReadStatus]:
    db_read_status = ReadStatus(item_id=item_id, user_id=user_id, is_read=is_read)
    session.add(db_read_status)
    await session.commit()
    await session.refresh(db_read_status)
    return db_read_status


async def get_item_read_status(
    session: AsyncSession, item_id: int, user_id: int
) -> Optional[ReadStatus]:
    query = select(ReadStatus).where(
        ReadStatus.item_id == item_id, ReadStatus.user_id == user_id
    )
    result = await session.execute(query)
    return result.scalar_one_or_none()


async def update_item_read_status(
    session: AsyncSession, item_id: int, user_id: int, is_read: bool
) -> Optional[ReadStatus]:
    db_item_read_status = await get_item_read_status(session, item_id, user_id)
    if not db_item_read_status:
        new_status = await create_read_status(session, item_id, user_id, is_read)
        return new_status

    db_item_read_status.is_read = is_read
    await session.commit()
    await session.refresh(db_item_read_status)
    return db_item_read_status
