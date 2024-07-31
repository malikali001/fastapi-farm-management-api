from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import auth, dependencies, models, schemas

router = APIRouter()


@router.post("/", response_model=schemas.users.User)
def create_user(
    user: schemas.users.UserCreate, db: Session = Depends(dependencies.get_db)
):
    db_user = models.User.get_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    user.password = auth.get_password_hash(user.password)
    return models.User.create(db=db, user=user)


@router.get("/me/", response_model=schemas.users.User)
async def read_users_me(
    current_user: models.User = Depends(auth.get_current_active_user),
):
    return current_user


@router.get("/{user_id}", response_model=schemas.users.User)
def read_user(user_id: int, db: Session = Depends(dependencies.get_db)):
    db_user = models.User.get_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.put("/{user_id}", response_model=schemas.users.User)
def update_user(
    user_id: int,
    user: schemas.users.UserCreate,
    db: Session = Depends(dependencies.get_db),
):
    db_user = models.User.get_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return models.User.update(db=db, user_id=user_id, user=user)


@router.delete("/{user_id}", response_model=schemas.users.User)
def delete_user(user_id: int, db: Session = Depends(dependencies.get_db)):
    db_user = models.User.get_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return models.User.delete(db=db, user_id=user_id)


@router.get("/", response_model=list[schemas.users.User])
def read_users(
    skip: int = 0, limit: int = 10, db: Session = Depends(dependencies.get_db)
):
    users = models.User.get(db, skip=skip, limit=limit)
    return users
