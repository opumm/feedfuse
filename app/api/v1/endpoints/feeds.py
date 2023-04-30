from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.api.deps import get_current_user
from app.db.session import get_async_session
from app.models.users import User as DBUser
from app.schemas import CreateFeedSchema, FeedSchema

router = APIRouter()


@router.get(
    path="/",
    response_model=List[FeedSchema],
    name="get_feeds",
    summary="Get all feeds subscribed by the current user",
    status_code=status.HTTP_200_OK,
)
async def get_feeds(
        session: AsyncSession = Depends(get_async_session),
        current_user: DBUser = Depends(get_current_user),
) -> List[FeedSchema]:
    """
    Retrieve all feeds that the current user has subscribed to.

    Returns:
        A list of FeedSchema objects containing the url and title of the subscribed feeds.
    """
    feeds_in_db = await crud.feeds.get_feed_by_user(session, user_id=current_user.id)
    feeds = [FeedSchema.from_orm(feed) for feed in feeds_in_db]
    return feeds


@router.post(
    path="/",
    response_model=FeedSchema,
    name="create_feed",
    summary="Create or subscribe to an RSS feed",
    status_code=status.HTTP_201_CREATED,
)
async def create_feed(
        feed: CreateFeedSchema,
        session: AsyncSession = Depends(get_async_session),
        current_user: DBUser = Depends(get_current_user),
) -> FeedSchema:
    """
    Create a new RSS feed or subscribe to an existing one.

    Args:
        feed: A CreateFeedSchema object containing the url and title of the feed to be created or subscribed to.

    Returns:
        A FeedSchema object containing the url and title of the created or subscribed feed.
        :param current_user:
        :param session:
        :param feed:
    """

    db_feed = await crud.feeds.get_feed_by_url(session, url=feed.url)
    if db_feed:
        db_subscription = await crud.subscription.get_subscription_by_user_and_feed(
            session, feed_id=db_feed.id, user_id=current_user.id
        )
        if db_subscription:
            if not db_subscription.is_active:
                await crud.subscription.resubscribe(
                    session, subscription_id=db_subscription.id
                )
        else:
            await crud.subscription.create_subscription(
                session, feed_id=db_feed.id, user_id=current_user.id
            )
    else:
        db_feed = await crud.feeds.create_feed(session, feed)
        await crud.subscription.create_subscription(
            session, feed_id=db_feed.id, user_id=current_user.id
        )

    return FeedSchema.from_orm(db_feed)


@router.get(
    path="/{feed_id}",
    response_model=FeedSchema,
    name="get_feed_by_id",
    summary="Get a specific feed by its ID",
    status_code=status.HTTP_200_OK,
)
async def get_feed_by_id(
        feed_id: int,
        session: AsyncSession = Depends(get_async_session)
) -> FeedSchema:
    """
    Retrieve a specific feed by its ID.

    Args:
        feed_id: The ID of the feed to be retrieved.

    Returns:
        A FeedSchema object containing the url and title of the requested feed.
        :param feed_id:
        :param session:
    """
    db_feed = await crud.feeds.get_feed(session, feed_id)
    if not db_feed:
        raise HTTPException(
            status_code=404,
            detail="Feed does not exist in the system",
        )

    return FeedSchema.from_orm(db_feed)


@router.delete(
    path="/{feed_id}",
    name="unsubscribe_feed",
    summary="Unsubscribe from a feed by its ID",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def unsubscribe_feed(feed_id: int) -> None:
    """
    Unsubscribe from a feed by its ID.

    Args:
        feed_id: The ID of the feed to be unsubscribed from.
    """

    # TODO: Implement the unsubscribe logic
    pass


@router.put(
    path="/{feed_id}/force-update",
    response_model=FeedSchema,
    name="force_update_feed",
    summary="Enable auto-update and trigger a force update",
    status_code=status.HTTP_202_ACCEPTED,
)
async def force_update_feed(feed_id: int) -> FeedSchema:
    """
    Enable auto-update and trigger a force update of the specified feed.

    Args:
        feed_id: The ID of the feed to be updated.

    Returns:
        A FeedSchema object containing the url and title of the updated feed.
    """

    # TODO: Implement the force update logic
    return FeedSchema(
        id=1,
        url="https://example.com/rss",
        title="New RSS feed",
        description="A new RSS feed for testing purposes.",
        is_update_enabled=True,
        created_at=datetime.now(),
    )
