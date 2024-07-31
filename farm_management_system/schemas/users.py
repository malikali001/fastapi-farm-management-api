from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserType(str, Enum):
    admin = "admin"
    manager = "manager"


class UserBase(BaseModel):
    email: EmailStr
    first_name: str = Field(..., max_length=30)
    last_name: str = Field(..., max_length=30)
    user_type: UserType


class UserCreate(UserBase):
    password: str


class UserInDBBase(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True


class User(UserInDBBase):
    pass


class UserInDB(UserInDBBase):
    hashed_password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None
