from ..database import models
from sqlalchemy import delete, select, update
from sqlalchemy.orm import Session
from typing import Any
from ..validation import schemas
from sqlalchemy import Row, Sequence, RowMapping

TASK_FIELDS = [
    models.RecurringTask.user_task_id,
    models.RecurringTask.name,
    models.RecurringTask.description,
    models.RecurringTask.priority,
    models.RecurringTask.days,
    models.RecurringTask.is_completed,
    models.RecurringTask.date_created,
]


def complete_uncomplete_recur_task(
    user_task_id: int, user_id: int, db: Session
) -> Row[Any]:
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


def create_recur_task(
    body: schemas.RecurTaskWithOwner, db: Session
) -> models.RecurringTask:
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


def get_recur_tasks(user_id: int, db: Session) -> Sequence[RowMapping]:
    tasks = (
        db.execute(select(*TASK_FIELDS).where(models.RecurringTask.owner == user_id))
        .mappings()
        .all()
    )
    return tasks


def get_recur_task(user_id: int, user_task_id: int, db: Session) -> RowMapping:
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


def update_recur_task(
    user_task_id: int, body: schemas.RecurTaskWithOwner, db: Session
) -> Row[Any]:
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


def delete_recur_task(user_id: int, user_task_id: int, db: Session) -> Row[tuple[int]]:
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
