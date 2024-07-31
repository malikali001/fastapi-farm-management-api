from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import dependencies, models, schemas

router = APIRouter()


@router.get("/", response_model=list[schemas.goats.Goat])
def read_goats(
    skip: int = 0, limit: int = 10, db: Session = Depends(dependencies.get_db)
):
    goats = models.Goat.get(db, skip=skip, limit=limit)
    return goats


@router.get("/{goat_id}", response_model=schemas.goats.Goat)
def read_goat(goat_id: int, db: Session = Depends(dependencies.get_db)):
    db_goat = models.Goat.get_by_id(db, goat_id=goat_id)
    if db_goat is None:
        raise HTTPException(status_code=404, detail="Goat not found")
    return db_goat


@router.post("/", response_model=schemas.goats.Goat)
def create_goat(
    goat: schemas.goats.GoatCreate, db: Session = Depends(dependencies.get_db)
):
    return models.Goat.create(db=db, goat=goat)


@router.put("/{goat_id}", response_model=schemas.goats.Goat)
def update_goat(
    goat_id: int,
    goat: schemas.goats.GoatUpdate,
    db: Session = Depends(dependencies.get_db),
):
    db_goat = models.Goat.update(db, goat_id=goat_id, goat=goat)
    if db_goat is None:
        raise HTTPException(status_code=404, detail="Goat not found")
    return db_goat


@router.delete("/{goat_id}", response_model=schemas.goats.Goat)
def delete_goat(goat_id: int, db: Session = Depends(dependencies.get_db)):
    db_goat = models.Goat.delete(db, goat_id=goat_id)
    if db_goat is None:
        raise HTTPException(status_code=404, detail="Goat not found")
    return db_goat
