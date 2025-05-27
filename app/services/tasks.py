from ..database import models
from sqlalchemy import delete, select, update

TASK_FIELDS = (
    models.Task.id,
    models.Task.name,
    models.Task.description,
    models.Task.priority,
    models.Task.date_created,
)


def create_task(body, db):
    task = models.Task(**body.model_dump())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def get_tasks(db):
    task = db.execute(select(TASK_FIELDS)).mappings().all()
    return task


def get_task(id, db):
    task = (
        db.execute(select(TASK_FIELDS).where(models.Task.id == id)).mappings().first()
    )

    return task


def update_task(id, body, db):
    task = db.execute(
        update(models.Task)
        .where(models.Task.id == id)
        .returning(TASK_FIELDS)
        .values(**body.model_dump())
    ).first()

    db.commit()
    db.refresh(task)

    return task


def delete_task(id, db):
    task = db.execute(
        delete(models.Task).where(models.Task.id == id).returning(models.Task.id)
    ).first()
    db.commit()
    db.refresh(task)
    return task