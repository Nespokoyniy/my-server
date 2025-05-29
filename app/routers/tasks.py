from fastapi import Depends, HTTPException
from fastapi.routing import APIRouter
from ..database.database import get_db, Session
from ..validation import schemas
from ..services import tasks
from ..utils.exc import db_exc_check
from ..utils.dependencies import oauth2_scheme, verify_token


router = APIRouter(prefix="/api/tasks", tags=["Tasks", "API"])


@router.post("/", status_code=201)
def create_task(body: schemas.Task, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    verify_token(token)
    db_exc_check(tasks.create_task, (body, token, db))
    return {"message": "new task was created"}
    


@router.get("/", status_code=200)
def get_tasks(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    verify_token(token)
    tasks = tasks.get_tasks(db)
    return tasks


@router.get("/{id}", status_code=200)
def get_task(id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    verify_token(token)
    task = tasks.get_task(id, db)
    
    if not task:
        raise HTTPException(404, detail="task doesn't exist")
    
    return task


@router.put("/{id}", status_code=200)
def update_task(body: schemas.Task, id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    verify_token(token)
    db_exc_check(tasks.update_task, (id, body, db))
    return {"message": f"task {id} was updated"}
    


@router.delete("/{id}", status_code=204)
def delete_task(id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    verify_token(token)
    db_exc_check(tasks.delete_task, (id, db))