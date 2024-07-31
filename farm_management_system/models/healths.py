from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Session, relationship

from ..database import Base
from ..schemas import healths as schema


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

    @classmethod
    def get_by_id(cls, db: Session, health_id: int):
        return db.query(cls).filter(cls.id == health_id).first()

    @classmethod
    def get(cls, db: Session, skip: int = 0, limit: int = 10):
        return db.query(cls).offset(skip).limit(limit).all()

    @classmethod
    def create(cls, db: Session, health: schema.HealthCreate):
        db_health = Health(
            date=health.date,
            title=health.title,
            description=health.description,
            treatment=health.treatment,
            goat_id=health.goat_id,
            manager_id=health.manager_id
        )
        db.add(db_health)
        db.commit()
        db.refresh(db_health)
        return db_health

    @classmethod
    def update(cls, db: Session, health_id: int, health: schema.HealthUpdate):
        db_health = db.query(cls).filter(cls.id == health_id).first()
        if db_health is None:
            return None
        for key, value in health.dict(exclude_unset=True).items():
            setattr(db_health, key, value)
        db.commit()
        db.refresh(db_health)
        return db_health

    @classmethod
    def delete_health(cls, db: Session, health_id: int):
        db_health = db.query(cls).filter(cls.id == health_id).first()
        if db_health is None:
            return None
        db.delete(db_health)
        db.commit()
        return db_health
