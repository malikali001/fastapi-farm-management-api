import enum

from sqlalchemy import Boolean, Column, Enum, Integer, String
from sqlalchemy.orm import Session

from ..database import Base
from ..schema import users_schema


class UserType(enum.Enum):
    admin = "admin"
    manager = "manager"


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    user_type = Column(Enum(UserType), server_default="manager")

    @classmethod
    def get_user(cls, db: Session, user_id: int):
        return db.query(cls).filter(cls.id == user_id).first()

    @classmethod
    def get_user_by_email(cls, db: Session, email: str):
        return db.query(cls).filter(cls.email == email).first()

    @classmethod
    def get_users(cls, db: Session, skip: int = 0, limit: int = 10):
        return db.query(cls).offset(skip).limit(limit).all()

    @classmethod
    def create_user(cls, db: Session, user: users_schema.UserCreate):
        db_user = cls(
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            user_type=user.user_type,
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @classmethod
    def update_user(cls, db: Session, user_id: int, user: users_schema.UserUpdate):
        db_user = db.query(cls).filter(cls.id == user_id).first()
        if db_user is None:
            return None
        update_data = user.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
        return db_user

    @classmethod
    def delete_user(cls, db: Session, user_id: int):
        db_user = db.query(cls).filter(cls.id == user_id).first()
        if db_user is None:
            return None
        db.delete(db_user)
        db.commit()
        return db_user
