from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.db.session import get_async_session
from app.schemas import CreateUserSchema, UpdateUserSchema, UserSchema

router = APIRouter()


@router.get(
    path="/",
    name="user_list",
    summary="Retrieve a list of all users",
    response_model=List[UserSchema],
    status_code=status.HTTP_200_OK,
)
async def get_users(session: AsyncSession = Depends(get_async_session)) -> Any:
    """
    Retrieve a list of all users.
    """
    users_in_db = await crud.users.get_users(session=session)
    users = [UserSchema.from_orm(user) for user in users_in_db]
    return users


@router.post(
    path="/",
    name="create_user",
    summary="Create a new user",
    response_model=UserSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    user_in: CreateUserSchema, session: AsyncSession = Depends(get_async_session)
) -> Any:
    """
    Create a new user.

    Args:
        user_in (CreateUserSchema): The input data to create a new user.
        session (AsyncSession, optional): The SQLAlchemy async session object. Defaults to Depends(get_async_session).

    Returns:
        user (UserSchema): The created user data.

    Raises:
        HTTPException: If a user with the same email already exists in the system.
    """
    existing_user = await crud.users.get_user_by_email(
        session=session, email=user_in.email
    )
    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="The user exist with the same email in the system",
        )
    user = await crud.users.create_user(session=session, user=user_in)
    return UserSchema.from_orm(user)


@router.get(
    path="/{user_id}",
    name="get_user_by_id",
    summary="Retrieve a specific user by their ID",
    response_model=UserSchema,
    status_code=status.HTTP_200_OK,
)
async def get_user_by_id(
    user_id: int, session: AsyncSession = Depends(get_async_session)
) -> Any:
    """
    Retrieve a specific user by their ID.
    """
    user = await crud.users.get_user(session=session, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user does not exist in the system",
        )
    return UserSchema.from_orm(user)


@router.put(
    path="/{user_id}",
    name="update_user",
    summary="Update a specific user",
    response_model=UserSchema,
    status_code=status.HTTP_200_OK,
)
async def update(
    user_id: int,
    user: UpdateUserSchema | None = None,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Update a specific user.
    """
    if not user:
        raise HTTPException(status_code=400, detail="Request body required")

    updated_user = await crud.users.update_user(session, user_id, user)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserSchema.from_orm(updated_user)
