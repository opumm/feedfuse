from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models import Subscription


async def create_subscription(
    session: AsyncSession, user_id: int, feed_id: int, is_active: bool = True
) -> Subscription:
    subscription = Subscription(user_id=user_id, feed_id=feed_id, is_active=is_active)
    session.add(subscription)
    await session.commit()
    await session.refresh(subscription)
    return subscription


async def get_subscription(
    session: AsyncSession, subscription_id: int
) -> Optional[Subscription]:
    result = await session.execute(select(Subscription).filter_by(id=subscription_id))
    return result.scalar_one_or_none()


async def get_subscriptions(
    session: AsyncSession, user_id: int, skip: int = 0, limit: int = 100
) -> List[Subscription]:
    result = await session.execute(
        select(Subscription).filter_by(user_id=user_id).offset(skip).limit(limit)
    )
    return result.scalars().all()


async def update_subscription(
    session: AsyncSession, subscription_id: int, is_active: Optional[bool] = None
) -> Optional[Subscription]:
    subscription = await get_subscription(session, subscription_id)
    if not subscription:
        return None
    if is_active is not None:
        subscription.is_active = is_active
    await session.commit()
    await session.refresh(subscription)
    return subscription


async def delete_subscription(
    session: AsyncSession, subscription_id: int
) -> Optional[Subscription]:
    subscription = await get_subscription(session, subscription_id)
    if not subscription:
        return None
    session.delete(subscription)
    await session.commit()
    return subscription
