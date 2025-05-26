from fastapi import Depends, HTTPException
from fastapi.routing import APIRouter
from ..database.database import get_db, Session
from ..validation import schemas
from ..database import models
from sqlalchemy import delete, select, update

router = APIRouter(prefix="/api/tasks")


@router.post("/", status_code=201)
def create_task(body: schemas.Task, db: Session = Depends(get_db)):
    task = models.Task(**body.model_dump())
    db.add(task)
    db.commit()

    return {"message": "new task was created"}


@router.get("/", status_code=200)
def get_tasks(db: Session = Depends(get_db)):
    tasks = (
        db.execute(
            select(
                models.Task.id,
                models.Task.name,
                models.Task.description,
                models.Task.priority,
                models.Task.date_created,
            )
        )
        .mappings()
        .all()
    )
    return tasks


@router.get("/{id}", status_code=200)
def get_task(id: int, db: Session = Depends(get_db)):
    task = (
        db.execute(
            select(
                models.Task.id,
                models.Task.name,
                models.Task.description,
                models.Task.priority,
                models.Task.date_created,
            ).where(models.Task.id == id)
        )
        .mappings()
        .first()
    )

    if not task:
        raise HTTPException(404, detail="task doesn't exist")

    return task


@router.put("/{id}", status_code=200)
def update_task(body: schemas.Task, id: int, db: Session = Depends(get_db)):
    task = db.execute(
        update(models.Task)
        .where(models.Task.id == id)
        .returning(
            models.Task.id,
            models.Task.name,
            models.Task.description,
            models.Task.priority,
            models.Task.date_created,
        )
        .values(**body.model_dump())
    )

    if not task:
        raise HTTPException(404, detail="task doesn't exist")

    db.commit()
    return {"message": f"task {id} was updated"}


@router.delete("/{id}", status_code=204)
def delete_task(id: int, db: Session = Depends(get_db)):
    task = db.execute(
        delete(models.Task).where(models.Task.id == id).returning(models.Task.id)
    ).first()

    if not task:
        raise HTTPException(404, detail="task doesn't exist")

    db.commit()
    return task
