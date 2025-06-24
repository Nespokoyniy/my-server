from fastapi import Depends, HTTPException
from fastapi.routing import APIRouter
from ..database.database import get_db, Session
from ..validation import schemas
from ..services import tasks
from ..utils.exc import db_exc_check
from ..utils.dependencies import get_current_user


router = APIRouter(prefix="/api/tasks", tags=["Tasks", "API"])


@router.post("/", status_code=201)
def create_task(
    body: schemas.Task,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    body = schemas.TaskWithOwner(**body.model_dump(), owner=user_id)
    db_exc_check(tasks.create_task, {"body": body, "db": db})
    return {"message": "new task was created"}


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

    if not task or task is None:
        raise HTTPException(404, detail="you don't have such task")

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

    if not updated_task or updated_task is None:
        raise HTTPException(404, detail="you don't have such task")

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

    if not task or task is None:
        raise HTTPException(404, detail="you don't have such task")
