from fastapi import Depends, HTTPException
from fastapi.routing import APIRouter
from ..validation import schemas
from ..database.database import get_db
from sqlalchemy.orm import Session
from ..utils.exc import db_exc_check
from ..services import recurring_tasks as rt
from ..utils.dependencies import get_current_user

router = APIRouter(prefix="/api/recur-tasks", tags=["Recur-tasks", "API"])


@router.put("/{user_task_id}/status", status_code=200)
def complete_uncomplete_recur_task(
    user_task_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    resp = db_exc_check(
        rt.complete_uncomplete_recur_task,
        {"db": db, "user_task_id": user_task_id, "user_id": user_id},
    )
    return resp


@router.post("/", status_code=201)
def create_recur_task(
    body: schemas.RecurTask,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    body = schemas.TaskWithOwner(**body.model_dump(), owner=user_id)
    resp = db_exc_check(rt.create_recur_task, {"body": body, "db": db})
    return resp


@router.get("/", status_code=200)
def get_recur_tasks(
    db: Session = Depends(get_db), user_id: int = Depends(get_current_user)
):
    tasks = rt.get_recur_tasks(user_id, db)
    return tasks


@router.get("/{user_task_id}", status_code=200)
def get_recur_task(
    user_task_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    task = rt.get_recur_task(user_id, user_task_id, db)

    if task is None:
        raise HTTPException(404, detail="the recurring task doesn't exist")

    return task


@router.put("/{user_task_id}", status_code=200)
def update_task(
    body: schemas.RecurTask,
    user_task_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    body = schemas.TaskWithOwner(**body.model_dump(), owner=user_id)
    task = db_exc_check(
        rt.update_recur_task, {"body": body, "db": db, "user_task_id": user_task_id}
    )

    if task is None:
        raise HTTPException(404, detail="the recurring task doesn't exist")

    return task


@router.delete("/{user_task_id}", status_code=204)
def delete_task(
    user_task_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    task = db_exc_check(
        rt.delete_recur_task,
        {"user_id": user_id, "user_task_id": user_task_id, "db": db},
    )

    if task is None:
        raise HTTPException(404, detail="the recurring task doesn't exist")

    return
