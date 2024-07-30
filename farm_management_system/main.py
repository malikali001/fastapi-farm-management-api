from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from . import auth, dependencies, models, schemas
from .database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.post("/token", response_model=schemas.users.Token)
async def login_for_access_token(db: Session = Depends(dependencies.get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = auth.timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/users/", response_model=schemas.users.User)
def create_user(user: schemas.users.UserCreate, db: Session = Depends(dependencies.get_db)):
    db_user = models.User.get_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    user.password = auth.get_password_hash(user.password)
    return models.User.create(db=db, user=user)


@app.get("/users/me/", response_model=schemas.users.User)
async def read_users_me(current_user: models.User = Depends(auth.get_current_active_user)):
    return current_user


@app.get("/users/{user_id}", response_model=schemas.users.User)
def read_user(user_id: int, db: Session = Depends(dependencies.get_db)):
    db_user = models.User.get_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.put("/users/{user_id}", response_model=schemas.users.User)
def update_user(user_id: int, user: schemas.users.UserCreate, db: Session = Depends(dependencies.get_db)):
    db_user = models.User.get_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return models.User.update(db=db, user_id=user_id, user=user)


@app.delete("/users/{user_id}", response_model=schemas.users.User)
def delete_user(user_id: int, db: Session = Depends(dependencies.get_db)):
    db_user = models.User.get_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return models.User.delete(db=db, user_id=user_id)


@app.get("/users/", response_model=list[schemas.users.User])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(dependencies.get_db)):
    users = models.User.get(db, skip=skip, limit=limit)
    return users
