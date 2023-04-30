from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models import Subscription


async def get_subscription(
    session: AsyncSession, subscription_id: int
) -> Optional[Subscription]:
    statement = select(Subscription).where(Subscription.id == subscription_id)
    result = await session.execute(statement)
    return result.scalars().first()


async def get_subscription_by_user_and_feed(
    session: AsyncSession, feed_id: int, user_id: int
) -> Optional[Subscription]:
    statement = select(Subscription).where(
        Subscription.feed_id == feed_id, Subscription.user_id == user_id
    )
    result = await session.execute(statement)
    return result.scalar_one_or_none()


async def resubscribe(
    session: AsyncSession, subscription_id: int
) -> Optional[Subscription]:
    db_subscription = await get_subscription(session, subscription_id)
    if not db_subscription:
        return None
    if db_subscription.is_active:
        return db_subscription

    setattr(db_subscription, "is_active", True)
    await session.commit()
    await session.refresh(db_subscription)
    return db_subscription


async def create_subscription(
    session: AsyncSession, feed_id: int, user_id: int
) -> Optional[Subscription]:
    existing_subscription = await get_subscription_by_user_and_feed(
        session, feed_id, user_id
    )
    if existing_subscription:
        if not existing_subscription.is_active:
            await resubscribe(existing_subscription.id)
        return existing_subscription

    db_subscription = Subscription(is_active=True, user_id=user_id, feed_id=feed_id)
    session.add(db_subscription)
    await session.commit()
    await session.refresh(db_subscription)
    return db_subscription


async def unsubscribe(
    session: AsyncSession, feed_id: int, user_id: int
) -> Optional[Subscription]:
    existing_subscription = await get_subscription_by_user_and_feed(
        session, feed_id, user_id
    )
    if existing_subscription:
        if existing_subscription.is_active:
            setattr(existing_subscription, "is_active", False)
            await session.commit()
            await session.refresh(existing_subscription)

        return existing_subscription
