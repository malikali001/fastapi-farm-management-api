from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from . import dependencies
from .auth import get_current_active_user
from .models import Goat, User


def is_admin(current_user: User = Depends(get_current_active_user)):
    if current_user.user_type != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
        )
    return current_user


def is_manager(current_user: User = Depends(get_current_active_user)):
    if current_user.user_type != "manager":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
        )
    return current_user


def is_admin_or_owner(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(dependencies.get_db),
    goat_id: int = None,
):
    if current_user.user_type == "admin":
        return current_user

    if current_user.user_type == "manager":
        goat = Goat.get_by_id(db, goat_id=goat_id)
        if goat and goat.manager_id == current_user.id:
            return current_user

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
    )
