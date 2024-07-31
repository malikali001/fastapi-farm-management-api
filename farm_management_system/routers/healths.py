from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import dependencies, models, schemas

router = APIRouter()


@router.get("/healths/", response_model=list[schemas.healths.Health])
def read_healths(skip: int = 0, limit: int = 10, db: Session = Depends(dependencies.get_db)):
    healths = models.Health.get(db, skip=skip, limit=limit)
    return healths


@router.get("/healths/{health_id}", response_model=schemas.healths.Health)
def read_health(health_id: int, db: Session = Depends(dependencies.get_db)):
    db_health = models.Health.get_by_id(db, health_id=health_id)
    if db_health is None:
        raise HTTPException(status_code=404, detail="Health record not found")
    return db_health


@router.post("/healths/", response_model=schemas.healths.Health)
def create_health(health: schemas.healths.HealthCreate, db: Session = Depends(dependencies.get_db)):
    return models.Health.create(db=db, health=health)


@router.put("/healths/{health_id}", response_model=schemas.healths.Health)
def update_health(health_id: int, health: schemas.healths.HealthUpdate, db: Session = Depends(dependencies.get_db)):
    db_health = models.Health.update(db, health_id=health_id, health=health)
    if db_health is None:
        raise HTTPException(status_code=404, detail="Health record not found")
    return db_health


@router.delete("/healths/{health_id}", response_model=schemas.healths.Health)
def delete_health(health_id: int, db: Session = Depends(dependencies.get_db)):
    db_health = models.Health.delete(db, health_id=health_id)
    if db_health is None:
        raise HTTPException(status_code=404, detail="Health record not found")
    return db_health
