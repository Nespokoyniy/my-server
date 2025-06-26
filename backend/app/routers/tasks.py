from fastapi import Depends, HTTPException
from fastapi.routing import APIRouter
from ..database.database import get_db, Session
from ..validation import schemas
from ..services import tasks
from ..utils.exc import db_exc_check
from ..utils.dependencies import get_current_user


router = APIRouter(prefix="/api/tasks", tags=["Tasks", "API"])


@router.put("/{user_task_id}/status", status_code=200)
def complete_uncomplete_task(
    user_task_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    resp = db_exc_check(
        tasks.complete_uncomplete_task,
        {"db": db, "user_task_id": user_task_id, "user_id": user_id},
    )
    return resp


@router.post("/", status_code=201)
def create_task(
    body: schemas.Task,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    body = schemas.TaskWithOwner(**body.model_dump(), owner=user_id)
    resp = db_exc_check(tasks.create_task, {"body": body, "db": db})
    return resp


@router.get("/", status_code=200)
def get_tasks(db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):
    my_tasks = tasks.get_tasks(user_id, db)
    return my_tasks


@router.get("/{task_id}", status_code=200)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    task = tasks.get_task(user_id, task_id, db)

    if task is None:
        raise HTTPException(404, detail="the task doesn't exist")

    return task


@router.put("/{task_id}", status_code=200)
def update_task(
    body: schemas.Task,
    task_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    body = schemas.TaskWithOwner(**body.model_dump(), owner=user_id)
    updated_task = db_exc_check(
        tasks.update_task, {"task_id": task_id, "body": body, "db": db}
    )

    if updated_task is None:
        raise HTTPException(404, detail="the task doesn't exist")

    return updated_task


@router.delete("/{task_id}", status_code=204)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    task = db_exc_check(
        tasks.delete_task, {"user_id": user_id, "task_id": task_id, "db": db}
    )

    if task is None:
        raise HTTPException(404, detail="the task doesn't exist")

    return
