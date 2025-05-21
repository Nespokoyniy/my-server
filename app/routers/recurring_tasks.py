from fastapi import Depends
from fastapi.routing import APIRouter
from validation import schemas
from database import models
from app.database.database import get_db, Session

router = APIRouter(prefix="/api/recur-tasks")

@router.post("/")
def new_recur_task(body: schemas.RecurTask, db: Session = Depends(get_db)):
    task = models.RecurringTask(**body.model_dump())
    db.add(task)
    db.commit()
    