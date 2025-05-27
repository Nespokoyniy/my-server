from ..database import models
from sqlalchemy import delete, select, update

TASK_FIELDS = (
    models.RecurringTask.id,
    models.RecurringTask.name,
    models.RecurringTask.description,
    models.RecurringTask.priority,
    models.RecurringTask.days,
    models.RecurringTask.date_created,
)


def create_recur_task(body, db):
    task = models.RecurringTask(**body.model_dump())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def get_recur_tasks(db):
    task = db.execute(select(TASK_FIELDS)).mappings().all()
    return task


def get_recur_task(id, db):
    task = (
        db.execute(select(TASK_FIELDS).where(models.RecurringTask.id == id))
        .mappings()
        .first()
    )

    return task


def update_recur_task(id, body, db):
    task = db.execute(
        update(models.RecurringTask)
        .where(models.RecurringTask.id == id)
        .returning(TASK_FIELDS)
        .values(**body.model_dump())
    ).first()

    db.commit()
    db.refresh(task)

    return task


def delete_recur_task(id, db):
    task = db.execute(
        delete(models.RecurringTask)
        .where(models.RecurringTask.id == id)
        .returning(models.RecurringTask.id)
    ).first()
    
    db.commit()
    db.refresh(task)
    
    return task
