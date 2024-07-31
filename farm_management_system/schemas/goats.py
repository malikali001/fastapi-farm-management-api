from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class GoatBase(BaseModel):
    name: UUID
    breed: str
    date_of_birth: datetime
    manager_id: int


class GoatCreate(GoatBase):
    pass


class GoatUpdate(GoatBase):
    pass


class GoatInDBBase(GoatBase):
    id: int

    class Config:
        orm_mode = True


class Goat(GoatInDBBase):
    pass


class GoatInDB(GoatInDBBase):
    pass
