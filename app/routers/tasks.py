from fastapi import Depends
from fastapi.routing import APIRouter
from ..database.database import get_db, Session
from ..validation import schemas
from ..database import models
from sqlalchemy import select, update

router = APIRouter(prefix="/api/tasks")


@router.post("/")
def new_task(body: schemas.Task, db: Session = Depends(get_db)):
    task = models.Task(**body.model_dump())
    db.add(task)
    db.commit()


@router.get("/")
def get_tasks(db: Session = Depends(get_db)):
    tasks = db.execute(
        select(models.Task.name, models.Task.description, models.Task.priority,)
    ).all()
    return tasks


@router.get("/{id}")
def get_task(id: int, db: Session = Depends(get_db)):
    task = db.execute(
        select(models.Task.name, models.Task.description, models.Task.priority).where(models.Task.id == id)
    ).all()
    
    return task


@router.put("/{id}")
def update_task(body: schemas.Task, id: int, db: Session = Depends(get_db)):
    task = db.execute(
        update(models.Task).where(models.Task.id == id).values(**body.model_dump())
    )
    db.commit()
     
    return task