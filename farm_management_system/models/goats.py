from uuid import uuid4

from sqlalchemy import UUID, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Session, relationship

from ..database import Base
from ..schemas import goats as schema


class Goat(Base):
    __tablename__ = 'goats'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(UUID, unique=True, default=uuid4)
    breed = Column(String)
    date_of_birth = Column(DateTime(timezone=True))
    manager_id = Column(Integer, ForeignKey("users.id"))
    manager = relationship("User")

    @classmethod
    def get_by_id(cls, db: Session, goat_id: int):
        return db.query(cls).filter(cls.id == goat_id).first()

    @classmethod
    def get(cls, db: Session, skip: int = 0, limit: int = 10):
        return db.query(cls).offset(skip).limit(limit).all()

    @classmethod
    def create(cls, db: Session, goat: schema.GoatCreate):
        db_goat = cls(
            name=uuid4(),
            breed=goat.breed,
            date_of_birth=goat.date_of_birth,
            manager_id=goat.manager_id
        )
        db.add(db_goat)
        db.commit()
        db.refresh(db_goat)
        return db_goat

    @classmethod
    def update(cls, db: Session, goat_id: int, goat: schema.GoatUpdate):
        db_goat = db.query(cls).filter(cls.id == goat_id).first()
        if db_goat is None:
            return None
        for key, value in goat.dict(exclude_unset=True).items():
            setattr(db_goat, key, value)
        db.commit()
        db.refresh(db_goat)
        return db_goat

    @classmethod
    def delete(cls, db: Session, goat_id: int):
        db_goat = db.query(cls).filter(cls.id == goat_id).first()
        if db_goat is None:
            return None
        db.delete(db_goat)
        db.commit()
        return db_goat
