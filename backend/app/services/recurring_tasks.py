from ..database import models
from sqlalchemy import delete, select, update
from ..database.database import Session

TASK_FIELDS = [
    models.RecurringTask.id,
    models.RecurringTask.name,
    models.RecurringTask.description,
    models.RecurringTask.priority,
    models.RecurringTask.days,
    models.RecurringTask.date_created,
]


def create_recur_task(body, db: Session):
    task = models.RecurringTask(**body.model_dump())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def get_recur_tasks(user_id, db: Session):
    task = (
        db.execute(select(*TASK_FIELDS).where(models.RecurringTask.owner == user_id))
        .mappings()
        .all()
    )
    return task


def get_recur_task(user_id, task_id, db: Session):
    task = (
        db.execute(
            select(*TASK_FIELDS).where(
                models.RecurringTask.id == task_id,
                models.RecurringTask.owner == user_id,
            )
        )
        .mappings()
        .first()
    )

    return task


def update_recur_task(task_id, body, db: Session):
    task = db.execute(
        update(models.RecurringTask)
        .where(models.RecurringTask.id == task_id, models.RecurringTask.owner == body["owner"])
        .returning(*TASK_FIELDS)
        .values(**body.model_dump())
    ).first()

    db.commit()
    db.refresh(task)

    return task


def delete_recur_task(user_id, task_id, db: Session):
    task = db.execute(
        delete(models.RecurringTask)
        .where(models.RecurringTask.id == task_id, models.RecurringTask.owner == user_id)
        .returning(models.RecurringTask.id)
    ).first()

    db.commit()
    db.refresh(task)

    return task
