from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, status

from app.schemas import ItemQueryParams, ItemSchema

router = APIRouter()


@router.get(
    path="/",
    name="item_list",
    summary="Retrieve a list of all items from feeds subscribed by the current user",
    response_model=List[ItemSchema],
    status_code=status.HTTP_200_OK,
)
async def get_items(query: ItemQueryParams = Depends()) -> List[ItemSchema]:
    """
    Get a list of all items from feeds subscribed by the current user.

    Args:
        query: Optional query parameters to filter the items list.

    Returns:
        A list of ItemSchema objects containing information about each item.
    """

    # TODO: Implement the logic to retrieve the items list from subscribed feeds
    return [
        ItemSchema(
            id=1,
            title="New article",
            url="https://example.com/article",
            guid="12345",
            description="This is a new article",
            feed_id=1,
            published_at=datetime.now(),
        )
    ]


@router.get(
    path="/{item_id}",
    name="get_item_by_id",
    summary="Retrieve an item by ID",
    response_model=ItemSchema,
    status_code=status.HTTP_200_OK,
)
async def get_item_by_id(item_id: int) -> ItemSchema:
    """
    Get the item with the specified ID.

    Args:
        item_id: The ID of the item to retrieve.

    Returns:
        An ItemSchema object containing information about the retrieved item.
    """

    return ItemSchema(
        id=item_id,
        title="New article",
        url="https://example.com/article",
        guid="12345",
        description="This is a new article",
        feed_id=1,
        published_at=datetime.now(),
    )


@router.post(
    path="/{item_id}",
    name="update_item",
    summary="Update an item",
    response_model=ItemSchema,
    status_code=status.HTTP_200_OK,
)
async def update_item(item_id: int, update_read_status: str) -> ItemSchema:
    """
    Update the read status of an item

    Args:
        item_id: The ID of the item to be updated.
        update_read_status: A boolean value indicating whether the item has been read or not.

    Returns:
        An ItemSchema object containing the updated item information.
    """

    # TODO: Implement the update logic and parameters

    return ItemSchema(
        id=item_id,
        title="New article",
        url="https://example.com/article",
        guid="12345",
        description="This is a new article",
        feed_id=1,
        published_at=datetime.now(),
    )
