from fastapi import Depends, HTTPException
from fastapi.routing import APIRouter
from ..validation import schemas
from app.database.database import get_db, Session
from ..utils.exc import db_exc_check
from ..services import recurring_tasks as rt
from ..utils.dependencies import oauth2_scheme, verify_token

router = APIRouter(prefix="/api/recur-tasks", tags=["Recur-tasks", "API"])

@router.post("/", status_code=201)
def create_recur_task(body: schemas.RecurTask, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    user_id = verify_token(token)
    body = schemas.TaskWithOwner(**body.model_dump(), owner=user_id)
    db_exc_check(rt.create_recur_task, {"body": body, "db": db})
    return {"message": "new recurring task was created"}


@router.get("/", status_code=200)
def get_recur_tasks(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    user_id = verify_token(token)
    tasks = rt.get_recur_tasks(user_id, db)
    return tasks


@router.get("/{task_id}", status_code=200)
def get_recur_task(task_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    user_id = verify_token(token)
    task = rt.get_recur_task(user_id, task_id, db)

    if not task:
        raise HTTPException(404, detail="recurring task doesn't exist")

    return task


@router.put("/{task_id}", status_code=200)
def update_task(body: schemas.RecurTask, task_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    user_id = verify_token(token)
    body = schemas.TaskWithOwner(**body.model_dump(), owner=user_id)
    task = db_exc_check(rt.update_recur_task,  {"task_id": user_id, "body": body, "db": db})
    
    if not task or task is None:
        raise HTTPException(404, detail="you don't have such task")
    
    return {"message": f"recurring task {task_id} was updated"}


@router.delete("/{task_id}", status_code=204)
def delete_task(task_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    user_id = verify_token(token)
    task = db_exc_check(rt.delete_recur_task, {"user_id": user_id, "task_id": task_id, "db": db})
    
    if not task or task is None:
        raise HTTPException(404, detail="you don't have such task")