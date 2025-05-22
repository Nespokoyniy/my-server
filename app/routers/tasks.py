from fastapi import Depends, HTTPException
from fastapi.routing import APIRouter
from ..database.database import get_db, Session
from ..validation import schemas
from ..database import models
from sqlalchemy import delete, select, update

router = APIRouter(prefix="/api/tasks")


@router.post("/", status_code=200)
def new_task(body: schemas.Task, db: Session = Depends(get_db)):
    task = models.Task(**body.model_dump())
    db.add(task)
    db.commit()


@router.get("/", status_code=200)
def get_tasks(db: Session = Depends(get_db)):
    tasks = db.execute(
        select(models.Task.name, models.Task.description, models.Task.priority,)
    ).mappings().all()
    return tasks


@router.get("/{id}", status_code=200)
def get_task(id: int, db: Session = Depends(get_db)):
    task = db.execute(
        select(models.Task.name, models.Task.description, models.Task.priority).where(models.Task.id == id)
    ).mappings().first()
    
    if not task:
        raise HTTPException
    
    return task


@router.put("/{id}", status_code=200)
def update_task(body: schemas.Task, id: int, db: Session = Depends(get_db)):
    db.execute(
        update(models.Task).where(models.Task.id == id).values(**body.model_dump())
    )
    db.commit()
     
    return

@router.delete("/{id}", status_code=204)
def delete_task(id: int, db: Session = Depends(get_db)):
    db.execute(
        delete(models.Task).where(models.Task.id == id)
    )
    db.commit()
    
    return 