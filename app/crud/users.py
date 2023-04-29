from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models import User as DBUser
from app.schemas import CreateUserSchema, UpdateUserSchema


async def create_user(session: AsyncSession, user: CreateUserSchema) -> DBUser:
    db_user = DBUser(**user.dict())
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user


async def get_user(session: AsyncSession, user_id: int) -> Optional[DBUser]:
    result = await session.execute(select(DBUser).filter_by(id=user_id))
    return result.scalar_one_or_none()


async def get_user_by_email(session: AsyncSession, email: str) -> Optional[DBUser]:
    result = await session.execute(select(DBUser).filter_by(email=email))
    return result.scalar_one_or_none()


async def get_users(
    session: AsyncSession, skip: int = 0, limit: int = 100
) -> List[DBUser]:
    result = await session.execute(select(DBUser).offset(skip).limit(limit))
    return result.scalars().all()


async def update_user(
    session: AsyncSession, user_id: int, user: UpdateUserSchema
) -> Optional[DBUser]:
    db_user = await get_user(session, user_id)
    if not db_user:
        return None
    update_data = user.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_user, field, value)
    await session.commit()
    await session.refresh(db_user)
    return db_user
