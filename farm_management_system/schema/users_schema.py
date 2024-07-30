from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr


class UserType(str, Enum):
    admin = "admin"
    manager = "manager"


class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    user_type: UserType


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False


class UserInDBBase(UserBase):
    id: int
    is_active: bool
    is_superuser: bool

    class Config:
        from_attributes = True


class User(UserInDBBase):
    pass


class UserInDB(UserInDBBase):
    hashed_password: str
