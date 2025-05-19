from fastapi import Depends
from fastapi.routing import APIRouter
from ..database.db import get_db, Session
from ..validation import schemas
from ..database import models

router = APIRouter(prefix="/api/tasks")

@router.post("/")
def new_task(body: schemas.Task, db: Session = Depends(get_db)):
    task = models.Task(**body.model_dump())
    db.add(task)
    db.commit()