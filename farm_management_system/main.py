from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from .database import Base, engine
from .dependencies import get_db
from .models import User
from .schema import users_schema

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.post("/users/", response_model=users_schema.User)
def create_user(user: users_schema.UserCreate, db: Session = Depends(get_db)):
    db_user = User.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return User.create_user(db=db, user=user)


@app.get("/users/{user_id}", response_model=users_schema.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = User.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.put("/users/{user_id}", response_model=users_schema.User)
def update_user(user_id: int, user: users_schema.UserUpdate, db: Session = Depends(get_db)):
    db_user = User.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return User.update_user(db=db, user_id=user_id, user=user)


@app.delete("/users/{user_id}", response_model=users_schema.User)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = User.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return User.delete_user(db=db, user_id=user_id)


@app.get("/users/", response_model=list[users_schema.User])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = User.get_users(db, skip=skip, limit=limit)
    return users
