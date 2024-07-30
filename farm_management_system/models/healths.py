from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ..database import Base


class Health(Base):
    __tablename__ = 'healths'

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime(timezone=True))
    title = Column(String)
    description = Column(String)
    treatment = Column(String)
    goat_id = Column(Integer, ForeignKey("goats.id"))
    goat = relationship("Goat")
    manager_id = Column(Integer, ForeignKey("users.id"))
    manager = relationship("User")
