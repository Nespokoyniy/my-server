from ..database import models
from sqlalchemy import delete, select, update
from ..database.database import Session

TASK_FIELDS = [
    models.RecurringTask.user_task_id,
    models.RecurringTask.name,
    models.RecurringTask.description,
    models.RecurringTask.priority,
    models.RecurringTask.days,
    models.RecurringTask.is_completed,
    models.RecurringTask.date_created,
]


def complete_uncomplete_recur_task(user_task_id, user_id, db: Session):
    is_completed = db.execute(
        select(models.RecurringTask.is_completed).where(
            models.RecurringTask.user_task_id == user_task_id,
            models.RecurringTask.owner == user_id,
        )
    )
    reverse_is_completed = not is_completed

    resp = db.execute(
        update(models.RecurringTask.is_completed)
        .where(
            models.RecurringTask.user_task_id == user_task_id,
            models.RecurringTask.owner == user_id,
        )
        .returning(*TASK_FIELDS)
        .values(**{"is_completed": reverse_is_completed})
    ).first()

    return resp


def create_recur_task(body, db: Session):
    body = body.model_dump()
    last_task = (
        db.execute(
            select(models.Task)
            .where(models.Task.owner == body["owner"])
            .order_by(models.Task.user_task_id.desc())
        )
        .scalars()
        .first()
    )

    if last_task is None:
        user_task_id = 1
    else:
        user_task_id = last_task.user_task_id
        user_task_id += 1

    body["user_task_id"] = user_task_id
    task = models.RecurringTask(**body)
    db.add(task)
    db.commit()
    db.refresh(task)

    return task


def get_recur_tasks(user_id, db: Session):
    tasks = (
        db.execute(select(*TASK_FIELDS).where(models.RecurringTask.owner == user_id))
        .mappings()
        .all()
    )
    return tasks


def get_recur_task(user_id, user_task_id, db: Session):
    task = (
        db.execute(
            select(*TASK_FIELDS).where(
                models.RecurringTask.user_task_id == user_task_id,
                models.RecurringTask.owner == user_id,
            )
        )
        .mappings()
        .first()
    )

    return task


def update_recur_task(user_task_id, body, db: Session):
    task = db.execute(
        update(models.RecurringTask)
        .where(
            models.RecurringTask.user_task_id == user_task_id,
            models.RecurringTask.owner == body["owner"],
        )
        .returning(*TASK_FIELDS)
        .values(**body.model_dump())
    ).first()

    db.commit()
    db.refresh(task)

    return task


def delete_recur_task(user_id, user_task_id, db: Session):
    task = db.execute(
        delete(models.RecurringTask)
        .where(
            models.RecurringTask.user_task_id == user_task_id,
            models.RecurringTask.owner == user_id,
        )
        .returning(models.RecurringTask.id)
    ).first()

    db.commit()
    db.refresh(task)

    return task
