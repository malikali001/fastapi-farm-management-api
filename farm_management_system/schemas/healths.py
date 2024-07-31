from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class HealthBase(BaseModel):
    date: datetime
    title: str
    description: Optional[str] = None
    treatment: Optional[str] = None
    goat_id: int
    manager_id: int


class HealthCreate(HealthBase):
    pass


class HealthUpdate(HealthBase):
    pass


class HealthInDBBase(HealthBase):
    id: int

    class Config:
        orm_mode = True


class Health(HealthInDBBase):
    pass


class HealthInDB(HealthInDBBase):
    pass
