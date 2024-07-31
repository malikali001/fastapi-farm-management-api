from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from . import auth, dependencies, schemas
from .database import Base, engine
from .routers import goats, healths, users

Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(
    users.router, prefix="/users", dependencies=[Depends(auth.get_current_active_user)]
)
app.include_router(
    goats.router, prefix="/goats", dependencies=[Depends(auth.get_current_active_user)]
)
app.include_router(
    healths.router,
    prefix="/healths",
    dependencies=[Depends(auth.get_current_active_user)],
)


@app.post("/token", response_model=schemas.users.Token)
async def login_for_access_token(
    db: Session = Depends(dependencies.get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
):
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


@app.post("/logout")
async def logout(
    db: Session = Depends(dependencies.get_db), token: str = Depends(auth.oauth2_scheme)
):
    auth.blacklist_token(db, token)
    return {"msg": "Successfully logged out"}
