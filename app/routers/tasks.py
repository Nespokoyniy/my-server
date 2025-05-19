from fastapi import Depends
from fastapi.routing import APIRouter
from ..database.db import get_db, Session
from .. import schemas

router = APIRouter(prefix="api/tasks/")

@router.post("/")
def new_task(body: schemas.Task, db: Session = Depends(get_db)):
    return {"message": body}