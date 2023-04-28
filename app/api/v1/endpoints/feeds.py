from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, status

from app.schemas import CreateFeedSchema, FeedQueryParams, FeedSchema

router = APIRouter()


@router.get(
    path="/",
    response_model=List[FeedSchema],
    name="get_feeds",
    summary="Get all feeds subscribed by the current user",
    status_code=status.HTTP_200_OK,
)
async def get_feeds(query: FeedQueryParams = Depends()) -> List[FeedSchema]:
    """
    Retrieve all feeds that the current user has subscribed to.

    Returns:
        A list of FeedSchema objects containing the url and title of the subscribed feeds.
    """

    return [
        FeedSchema(
            id=1,
            url="https://example.com/rss",
            title="New RSS feed",
            description="A new RSS feed for testing purposes.",
            is_update_enabled=True,
            created_at=datetime.now(),
        ),
    ]


@router.post(
    path="/",
    response_model=FeedSchema,
    name="create_feed",
    summary="Create or subscribe to an RSS feed",
    status_code=status.HTTP_201_CREATED,
)
async def create_feed(feed: CreateFeedSchema) -> FeedSchema:
    """
    Create a new RSS feed or subscribe to an existing one.

    Args:
        feed: A CreateFeedSchema object containing the url and title of the feed to be created or subscribed to.

    Returns:
        A FeedSchema object containing the url and title of the created or subscribed feed.
        :param feed:
    """
    # TODO: Implement the creation or subscription logic
    return FeedSchema(
        id=1,
        url="https://example.com/rss",
        title="New RSS feed",
        description="A new RSS feed for testing purposes.",
        is_update_enabled=True,
        created_at=datetime.now(),
    )


@router.get(
    path="/{feed_id}",
    response_model=FeedSchema,
    name="get_feed_by_id",
    summary="Get a specific feed by its ID",
    status_code=status.HTTP_200_OK,
)
async def get_feed_by_id(feed_id: int) -> FeedSchema:
    """
    Retrieve a specific feed by its ID.

    Args:
        feed_id: The ID of the feed to be retrieved.

    Returns:
        A FeedSchema object containing the url and title of the requested feed.
    """

    return FeedSchema(
        id=1,
        url="https://example.com/rss",
        title="New RSS feed",
        description="A new RSS feed for testing purposes.",
        is_update_enabled=True,
        created_at=datetime.now(),
    )


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
