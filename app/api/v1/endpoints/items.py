from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.api.deps import get_current_user
from app.db.session import get_async_session
from app.models.users import User as DBUser
from app.schemas import ItemQueryParams, ItemSchema

router = APIRouter()


@router.get(
    path="/",
    name="item_list",
    summary="Retrieve a list of all items from feeds subscribed by the current user",
    response_model=List[ItemSchema],
    status_code=status.HTTP_200_OK,
)
async def get_items(
    query_params: ItemQueryParams = Depends(),
    session: AsyncSession = Depends(get_async_session),
    current_user: DBUser = Depends(get_current_user),
) -> List[ItemSchema]:
    """
    Get a list of all items from feeds subscribed by the current user.

    Args:
        query: Optional query parameters to filter the items list.

    Returns:
        A list of ItemSchema objects containing information about each item.
        :param query_params:
        :param current_user:
        :param session:
    """

    items = await crud.items.get_items(session, current_user.id, query_params)
    if not items:
        raise HTTPException(
            status_code=404,
            detail="No item exist in the system",
        )
    return [ItemSchema.from_orm(item) for item in items]


@router.get(
    path="/{item_id}",
    name="get_item_by_id",
    summary="Retrieve an item by ID",
    response_model=ItemSchema,
    status_code=status.HTTP_200_OK,
)
async def get_item_by_id(
    item_id: int, session: AsyncSession = Depends(get_async_session)
) -> ItemSchema:
    """
    Get the item with the specified ID.

    Args:
        item_id: The ID of the item to retrieve.

    Returns:
        An ItemSchema object containing information about the retrieved item.
        :param item_id:
        :param session:
    """
    item = await crud.items.get_item(session, item_id)
    if not item:
        raise HTTPException(
            status_code=404,
            detail="Item does not exist in the system",
        )

    return ItemSchema.from_orm(item)


@router.post(
    path="/{item_id}",
    name="update_item",
    summary="Update an item",
    response_model=ItemSchema,
    status_code=status.HTTP_200_OK,
)
async def update_item(
    item_id: int,
    mark_as_read: bool,
    session: AsyncSession = Depends(get_async_session),
    current_user: DBUser = Depends(get_current_user),
) -> ItemSchema:
    """
    Update the read status of an item

    Args:
        item_id: The ID of the item to be updated.
        update_read_status: A boolean value indicating whether the item has been read or not.

    Returns:
        An ItemSchema object containing the updated item information.
        :param item_id:
        :param current_user:
        :param session:
        :param mark_as_read:
    """

    item = await crud.items.get_item(session, item_id)
    if not item:
        raise HTTPException(
            status_code=404,
            detail="Item does not exist in the system",
        )

    await crud.read_status.update_item_read_status(
        session, item_id, current_user.id, mark_as_read
    )

    return ItemSchema.from_orm(item)
