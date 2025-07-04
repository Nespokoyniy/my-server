from ..database import models
from sqlalchemy import delete, select, update
from typing import Optional
from sqlalchemy.orm import Session
from ..validation import schemas
import datetime

TASK_FIELDS = [
    models.Task.user_task_id,
    models.Task.name,
    models.Task.description,
    models.Task.priority,
    models.Task.is_completed,
    models.Task.date_created,
]


def complete_uncomplete_task(
    user_task_id: int, user_id: int, db: Session
) -> Optional[schemas.TaskOut]:
    with db.begin():
        task = db.execute(
            select(models.Task.is_completed).where(
                models.Task.user_task_id == user_task_id, models.Task.owner == user_id
            )
        ).scalar_one_or_none()

        if task is None:
            return None

        resp = db.execute(
            update(models.Task)
            .where(
                models.Task.user_task_id == user_task_id, models.Task.owner == user_id
            )
            .returning(*TASK_FIELDS)
            .values(is_completed=not task.is_completed)
        ).first()

        resp = schemas.TaskOut(**resp._asdict())

        return resp


def create_task(body: schemas.TaskWithOwner, db: Session) -> schemas.TaskOut:
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
        task = models.Task(**body)
        db.add(task)
        db.flush()
        task = schemas.TaskOut.model_validate(**body)
        return task


def get_tasks(user_id: int, db: Session) -> list[schemas.TaskOut]:
    tasks = (
        db.execute(select(*TASK_FIELDS).where(models.Task.owner == user_id))
        .scalars()
        .all()
    )
    return [schemas.TaskOut(task) for task in tasks]


def get_task(user_id: int, user_task_id: int, db: Session) -> Optional[schemas.TaskOut]:
    task = (
        db.execute(
            select(*TASK_FIELDS).where(
                models.Task.user_task_id == user_task_id, models.Task.owner == user_id
            )
        )
        .scalars()
        .first()
    )

    if task:
        task = schemas.TaskOut(**task._asdict())
        return task

    return None


def update_task(
    user_task_id: int, body: schemas.TaskWithOwner, db: Session
) -> Optional[schemas.TaskOut]:
    with db.begin():
        task = db.execute(
            update(models.Task)
            .where(
                models.Task.user_task_id == user_task_id,
                models.Task.owner == body["owner"],
            )
            .returning(*TASK_FIELDS)
            .values(**body.model_dump())
        ).first()

        if task:
            task = schemas.TaskOut(**task._asdict())
            return task

        return None


def delete_task(
    user_id: int, user_task_id: int, db: Session
) -> Optional[schemas.TaskOut]:
    with db.begin():
        task = db.execute(
            delete(models.Task)
            .where(
                models.Task.user_task_id == user_task_id, models.Task.owner == user_id
            )
            .returning(models.Task.id)
        ).first()

        if task:
            task = schemas.TaskOut(**task._asdict())
            return task

        return None
