from ..database import models
from sqlalchemy import delete, select, update
from ..database.database import Session

TASK_FIELDS = [
    models.Task.id,
    models.Task.name,
    models.Task.description,
    models.Task.priority,
    models.Task.date_created,
]


def create_task(body, db: Session):
    task = models.Task(**body.model_dump())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def get_tasks(user_id, db: Session):
    task = (
        db.execute(select(*TASK_FIELDS).where(models.Task.owner == user_id))
        .mappings()
        .all()
    )
    return task


def get_task(user_id, task_id, db: Session):
    task = (
        db.execute(
            select(*TASK_FIELDS).where(
                models.Task.task_id == task_id, models.Task.owner == user_id
            )
        )
        .mappings()
        .first()
    )

    return task


def update_task(task_id, body, db: Session):
    task = db.execute(
        update(models.Task)
        .where(models.Task.id == task_id, models.Task.owner == body["owner"])
        .returning(*TASK_FIELDS)
        .values(**body.model_dump())
    ).first()

    db.commit()
    db.refresh(task)

    return task


def delete_task(user_id, id, db: Session):
    task = db.execute(
        delete(models.Task)
        .where(models.Task.id == id, models.Task.owner == user_id)
        .returning(models.Task.id)
    ).first()
    db.commit()
    db.refresh(task)
    return task
