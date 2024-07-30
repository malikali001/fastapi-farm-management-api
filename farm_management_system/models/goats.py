import uuid

from sqlalchemy import UUID, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ..database import Base


class Goat(Base):
    __tablename__ = 'goats'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(UUID, unique=True, default=uuid.uuid4)
    breed = Column(String)
    date_of_birth = Column(DateTime(timezone=True))
    manager_id = Column(Integer, ForeignKey("users.id"))
    manager = relationship("User")
