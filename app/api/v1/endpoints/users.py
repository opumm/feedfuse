from typing import List

from fastapi import APIRouter, status

from app.schemas import CreateUserSchema, UpdateUserSchema, UserSchema

router = APIRouter()


@router.get(
    path="/",
    name="user_list",
    summary="Retrieve a list of all users",
    response_model=List[UserSchema],
    status_code=status.HTTP_200_OK,
)
async def get_users():
    """
    Retrieve a list of all users.
    """
    return [{"id": 1, "email": "abc@example.com", "full_name": "Mr Abc"}]


@router.post(
    path="/",
    name="create_user",
    summary="Create a new user",
    response_model=UserSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(user: CreateUserSchema):
    """
    Create a new user.
    """
    _user = {"id": 1, "email": user.email, "full_name": user.full_name}

    return _user


@router.get(
    path="/{user_id}",
    name="get_user_by_id",
    summary="Retrieve a specific user by their ID",
    response_model=UserSchema,
    status_code=status.HTTP_200_OK,
)
async def get_user_by_id(user_id: int):
    """
    Retrieve a specific user by their ID.
    """
    return {"id": user_id, "email": "abc@example.com", "full_name": "Mr Abc"}


@router.put(
    path="/{user_id}",
    name="update_user",
    summary="Update a specific user",
    response_model=UserSchema,
    status_code=status.HTTP_200_OK,
)
async def update(user_id: int, user: UpdateUserSchema | None = None):
    """
    Update a specific user.
    """
    return {"id": user_id, "email": "abc@example.com", "full_name": "Mr Abc"}
