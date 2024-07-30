from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import Session

from ..database import Base


class BlacklistedToken(Base):
    __tablename__ = 'blacklisted_tokens'

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, unique=True, index=True)
    blacklisted_on = Column(DateTime, default=datetime.utcnow)

    @classmethod
    def is_blacklisted(cls, db: Session, token: str):
        return db.query(cls).filter(cls.token == token).first() is not None
