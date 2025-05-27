from fastapi import Depends, HTTPException
from fastapi.routing import APIRouter
from ..validation import schemas
from app.database.database import get_db, Session
from ..utils.exc import db_exc_check
from ..services import recurring_tasks as rt

router = APIRouter(prefix="/api/recur-tasks")

@router.post("/", status_code=201)
def create_recur_task(body: schemas.RecurTask, db: Session = Depends(get_db)):
    db_exc_check(rt.create_recur_task, (body, db))
    return {"message": "new recurring task was created"}


@router.get("/", status_code=200)
def get_recur_tasks(db: Session = Depends(get_db)):
    tasks = rt.get_recur_tasks(db)
    return tasks


@router.get("/{id}", status_code=200)
def get_recur_task(id: int, db: Session = Depends(get_db)):
    task = rt.get_recur_task(id, db)

    if not task:
        raise HTTPException(404, detail="recurring task doesn't exist")

    return task


@router.put("/{id}", status_code=200)
def update_task(body: schemas.RecurTask, id: int, db: Session = Depends(get_db)):
    db_exc_check(rt.update_recur_task, (id, body, db))
    return {"message": f"recurring task {id} was updated"}


@router.delete("/{id}", status_code=204)
def delete_task(id: int, db: Session = Depends(get_db)):
    db_exc_check(rt.delete_recur_task, (id, db))