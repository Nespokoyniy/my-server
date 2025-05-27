from ..database import models
from sqlalchemy import delete, select, update

# добавь проверку прав Admin

USER_FIELDS = (
    models.User.id,
    models.User.email,
    models.User.name,
    models.User.date_created,
)


def create_user(body, db):
    body = body.model_dump()
    user = models.User(**body)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user(id, db):
    user = (
        db.execute(select(USER_FIELDS).where(models.User.id == id)).mappings().first()
    )
    return user


def update_user(id, body, db):
    user = db.execute(
        update(models.User)
        .where(models.User.id == id)
        .returning(USER_FIELDS)
        .values(**body.model_dump())
    ).first()

    db.commit()
    db.refresh(user)

    return user


def delete_user(id, db):
    user = db.execute(
        delete(models.User).where(models.User.id == id).returning(models.User.id)
    ).first()
    db.commit()
    db.refresh(user)
    return user
