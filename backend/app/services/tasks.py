from ..database import models
from sqlalchemy import Row, RowMapping, Sequence, delete, select, update
from typing import Any
from sqlalchemy.orm import Session
from ..validation import schemas

TASK_FIELDS = [
    models.Task.user_task_id,
    models.Task.name,
    models.Task.description,
    models.Task.priority,
    models.Task.is_completed,
    models.Task.date_created,
]


def complete_uncomplete_task(user_task_id: int, user_id: int, db: Session) -> Row[Any] | None:
    is_completed = db.execute(
        select(models.Task.is_completed).where(
            models.Task.user_task_id == user_task_id, models.Task.owner == user_id
        )
    ).scalar_one_or_none()
    
    if is_completed is None:
        return None

    resp = db.execute(
        update(models.Task.is_completed)
        .where(models.Task.user_task_id == user_task_id, models.Task.owner == user_id)
        .returning(*TASK_FIELDS)
        .values(is_completed=not is_completed)
    ).first()
    
    db.commit()
    return resp


def create_task(body: schemas.TaskWithOwner, db: Session) -> models.Task:
    body = body.model_dump()
    last_task = (
        db.execute(
            select(models.Task)
            .where(models.Task.owner == body["owner"])
            .order_by(models.Task.user_task_id.desc())
        )
        .scalar_one_or_none()
    )

    if last_task is None:
        user_task_id = 1
    else:
        user_task_id = last_task.user_task_id
        user_task_id += 1

    body["user_task_id"] = user_task_id
    task = models.Task(**body)
    db.add(task)
    db.commit()
    db.refresh(task)

    return task


def get_tasks(user_id: int, db: Session) -> Sequence[RowMapping]:
    tasks = (
        db.execute(select(*TASK_FIELDS).where(models.Task.owner == user_id))
        .mappings()
        .all()
    )
    return tasks


def get_task(user_id: int, user_task_id: int, db: Session) -> RowMapping:
    task = (
        db.execute(
            select(*TASK_FIELDS).where(
                models.Task.user_task_id == user_task_id, models.Task.owner == user_id
            )
        )
        .mappings()
        .first()
    )

    return task[0] if task else None


def update_task(
    user_task_id: int, body: schemas.TaskWithOwner, db: Session
) -> Row[Any]:
    task = db.execute(
        update(models.Task)
        .where(
            models.Task.user_task_id == user_task_id, models.Task.owner == body["owner"]
        )
        .returning(*TASK_FIELDS)
        .values(**body.model_dump())
    ).first()

    db.commit()
    db.refresh(task)

    return task[0] if task else None


def delete_task(user_id: int, user_task_id: int, db: Session) -> Row[tuple[int]] | None:
    task = db.execute(
        delete(models.Task)
        .where(models.Task.user_task_id == user_task_id, models.Task.owner == user_id)
        .returning(models.Task.id)
    ).first()

    db.commit()
    
    return task[0] if task else None