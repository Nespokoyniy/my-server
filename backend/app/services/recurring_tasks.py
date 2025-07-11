from fastapi import Response
from ..database import models
from sqlalchemy import delete, select, update
from sqlalchemy.orm import Session
from typing import Optional
from ..validation import schemas
import datetime

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
) -> Optional[schemas.RecurTaskOut]:
    task = db.execute(
        select(models.RecurringTask).where(
            models.RecurringTask.user_task_id == user_task_id,
            models.RecurringTask.owner == user_id,
        )
    ).scalar_one_or_none()

    if task is None:
        return None

    resp = db.execute(
        update(models.RecurringTask)
        .where(
            models.RecurringTask.user_task_id == user_task_id,
            models.RecurringTask.owner == user_id,
        )
        .returning(*TASK_FIELDS)
        .values(is_completed=not task.is_completed)
    ).first()

    db.commit()
    return schemas.RecurTaskOut.model_validate(resp)


def create_recur_task(
    body: schemas.RecurTaskWithOwner, db: Session
) -> schemas.RecurTaskOut:
    body = body.model_dump()
    body["date_created"] = datetime.datetime.now(datetime.timezone.utc)
    last_task = db.execute(
        select(models.RecurringTask.user_task_id)
        .where(models.RecurringTask.owner == body["owner"])
        .order_by(models.RecurringTask.user_task_id.desc())
        .limit(1)
    ).scalar_one_or_none()

    user_task_id = 1 if last_task is None else last_task + 1
    body["user_task_id"] = user_task_id

    task = models.RecurringTask(**body)
    db.add(task)
    db.commit()
    db.refresh(task)
    return schemas.RecurTaskOut.model_validate(task)


def get_recur_tasks(user_id: int, db: Session) -> list[schemas.RecurTaskOut]:
    tasks = (
        db.execute(
            select(models.RecurringTask).where(models.RecurringTask.owner == user_id)
        )
        .scalars()
        .all()
    )
    return [schemas.RecurTaskOut.model_validate(task) for task in tasks]


def get_recur_task(
    user_id: int, user_task_id: int, db: Session
) -> Optional[schemas.RecurTaskOut]:
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

    if task:
        return schemas.RecurTaskOut.model_validate(task)

    return None


def update_recur_task(
    user_task_id: int, body: schemas.RecurTaskWithOwner, db: Session
) -> Optional[schemas.RecurTaskOut]:
    task = db.execute(
        update(models.RecurringTask)
        .where(
            models.RecurringTask.user_task_id == user_task_id,
            models.RecurringTask.owner == body.owner,
        )
        .returning(*TASK_FIELDS)
        .values(**body.model_dump())
    ).first()

    if task:
        db.commit()
        return schemas.RecurTaskOut.model_validate(task)

    return None


def delete_recur_task(
    user_id: int, user_task_id: int, db: Session
) -> Optional[schemas.RecurTaskOut]:
    task_id = (
        db.execute(
            delete(models.RecurringTask)
            .where(
                models.RecurringTask.user_task_id == user_task_id,
                models.RecurringTask.owner == user_id,
            )
            .returning(models.RecurringTask.user_task_id)
        )
        .scalars()
        .first()
    )

    if task_id:
        db.commit()
        return task_id

    return None
