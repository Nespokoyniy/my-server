from fastapi import Depends, HTTPException
from fastapi.routing import APIRouter
from ..validation import schemas
from ..database import models
from app.database.database import get_db, Session
from sqlalchemy import delete, select, update

router = APIRouter(prefix="/api/recur-tasks")

@router.post("/", status_code=201)
def new_recur_task(body: schemas.RecurTask, db: Session = Depends(get_db)):
    task = models.RecurringTask(**body.model_dump())
    db.add(task)
    db.commit()
    
    return {"message": "new recurring task was created"}

@router.get("/", status_code=200)
def get_recur_tasks(db: Session = Depends(get_db)):
    tasks = (
        db.execute(
            select(
                models.RecurringTask.id,
                models.RecurringTask.name,
                models.RecurringTask.description,
                models.RecurringTask.priority,
                models.RecurringTask.days,
                models.RecurringTask.date_created,
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
                models.RecurringTask.id,
                models.RecurringTask.name,
                models.RecurringTask.description,
                models.RecurringTask.priority,
                models.RecurringTask.days,
                models.RecurringTask.date_created,
            ).where(models.RecurringTask.id == id)
        )
        .mappings()
        .first()
    )

    if not task:
        raise HTTPException(404, detail="task doesn't exist")

    return task


@router.put("/{id}", status_code=200)
def update_task(body: schemas.RecurTask, id: int, db: Session = Depends(get_db)):
    task = db.execute(
        update(models.RecurringTask)
        .where(models.RecurringTask.id == id)
        .returning(models.RecurringTask.id,
            models.RecurringTask.name,
            models.RecurringTask.description,
            models.RecurringTask.priority,
            models.RecurringTask.date_created)
        .values(**body.model_dump())
    )

    if not task:
        raise HTTPException(404, detail="task doesn't exist")

    db.commit()
    return {"message": f"recurring task {id} was updated"}


@router.delete("/{id}", status_code=204)
def delete_task(id: int, db: Session = Depends(get_db)):
    task = db.execute(
        delete(models.RecurringTask).where(models.RecurringTask.id == id).returning(models.RecurringTask.id)
    ).first()

    if not task:
        raise HTTPException(404, detail="task doesn't exist")

    db.commit()
    return task
