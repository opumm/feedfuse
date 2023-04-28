from typing import Optional

from pydantic import BaseModel, EmailStr


# Shared properties
class UserBaseSchema(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None


# Properties to receive via API on creation
class CreateUserSchema(UserBaseSchema):
    email: EmailStr
    password: str


class UpdateUserSchema(UserBaseSchema):
    password: Optional[str] = None


class UserSchema(UserBaseSchema):
    id: Optional[int] = None

    class Config:
        orm_mode = True
