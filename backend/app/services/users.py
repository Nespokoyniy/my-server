from typing import Optional
from fastapi.security import OAuth2PasswordRequestForm
from ..utils.hash import verify_pwd
from sqlalchemy.orm import Session
from ..database import models
from sqlalchemy import delete, select, update
from ..validation import schemas

USER_FIELDS = [
    models.User.id,
    models.User.email,
    models.User.name,
    models.User.date_created,
]

USER_FIELDS_AND_PWD = USER_FIELDS.copy() + [models.User.password]


def create_user(body: schemas.User, db: Session) -> schemas.UserOut:
    with db.begin():
        body = body.model_dump()
        user = models.User(**body)
        db.add(user)
        user = schemas.UserOut(**body)
        return user


def get_user(user_id: int, db: Session) -> Optional[schemas.UserOut]:
    user = (
        db.execute(select(*USER_FIELDS).where(models.User.id == user_id))
        .scalars()
        .first()
    )

    if user:
        user = schemas.UserOut(**user._asdict())
        return user

    return None


def get_user_by_form(
    form: OAuth2PasswordRequestForm, db: Session
) -> Optional[schemas.UserOut]:
    users = (
        db.execute(
            select(*USER_FIELDS_AND_PWD).where(models.User.name == form.username)
        )
        .scalars()
        .all()
    )

    for user in users:
        if verify_pwd(form.password, user["password"]):
            user = schemas.UserOut(**user._asdict())
            return user

    return None


def update_user(user_id: int, body, db: Session) -> Optional[schemas.UserOut]:
    with db.begin():
        user = db.execute(
            update(models.User)
            .where(models.User.id == user_id)
            .returning(*USER_FIELDS)
            .values(**body.model_dump())
        ).first()

        if user:
            user = schemas.UserOut(**user._asdict())
            return user

        return None


def delete_user(user_id: int, db: Session) -> schemas.UserOut:
    with db.begin():
        user = (
            db.execute(
                delete(models.User)
                .where(models.User.id == user_id)
                .returning(models.User.id)
            )
            .scalars()
            .first()
        )

        user = schemas.UserOut(**user._asdict())
        return user