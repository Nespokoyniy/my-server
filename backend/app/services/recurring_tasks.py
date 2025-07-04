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
    with db.begin():
        task = db.execute(
            select(models.RecurringTask.is_completed).where(
                models.RecurringTask.user_task_id == user_task_id,
                models.RecurringTask.owner == user_id,
            )
        ).scalar_one_or_none()

        if task is None:
            return None

        resp = db.execute(
            update(models.RecurringTask.is_completed)
            .where(
                models.RecurringTask.user_task_id == user_task_id,
                models.RecurringTask.owner == user_id,
            )
            .returning(*TASK_FIELDS)
            .values(is_completed=not task.is_completed)
        ).first()

        return resp


def create_recur_task(
    body: schemas.RecurTaskWithOwner, db: Session
) -> schemas.RecurTaskOut:
    body = body.model_dump()
    body["date_created"] = datetime.datetime.now(datetime.timezone.utc)
    with db.begin():
        last_task = db.execute(
            select(models.Task)
            .where(models.Task.owner == body["owner"])
            .order_by(models.Task.user_task_id.desc())
            .with_for_update()
        ).scalar_one_or_none()

        user_task_id = 1 if last_task is None else last_task.user_task_id + 1

        body["user_task_id"] = user_task_id
        task = models.RecurringTask(**body)
        db.add(task)
        db.flush()
        task = schemas.RecurTaskOut.model_validate(**body)
        return task


def get_recur_tasks(user_id: int, db: Session) -> list[schemas.RecurTaskOut]:
    tasks = (
        db.execute(select(*TASK_FIELDS).where(models.RecurringTask.owner == user_id))
        .scalars()
        .all()
    )
    return [schemas.TaskOut(task) for task in tasks]


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
        .scalars()
        .first()
    )

    if task:
        task = schemas.RecurTaskOut(**task._asdict())
        return task

    return None


def update_recur_task(
    user_task_id: int, body: schemas.RecurTaskWithOwner, db: Session
) -> Optional[schemas.RecurTaskOut]:
    with db.begin():
        task = db.execute(
            update(models.RecurringTask)
            .where(
                models.RecurringTask.user_task_id == user_task_id,
                models.RecurringTask.owner == body["owner"],
            )
            .returning(*TASK_FIELDS)
            .values(**body.model_dump())
        ).first()

        if task:
            task = schemas.RecurTaskOut(**task._asdict())
            return task

        return None


def delete_recur_task(
    user_id: int, user_task_id: int, db: Session
) -> Optional[schemas.RecurTaskOut]:
    with db.begin():
        task = db.execute(
            delete(models.RecurringTask)
            .where(
                models.RecurringTask.user_task_id == user_task_id,
                models.RecurringTask.owner == user_id,
            )
            .returning(models.RecurringTask.id)
        ).first()

        if task:
            task = schemas.RecurTaskOut(**task._asdict())
            return task

        return None
