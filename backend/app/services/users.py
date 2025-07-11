from typing import Optional
from fastapi.security import OAuth2PasswordRequestForm
# from backend.app.utils.dependencies import send_code
from ..utils.hash import verify_pwd
from sqlalchemy.orm import Session
from ..database import models
from sqlalchemy import delete, select, update
from ..validation import schemas
import datetime
from fastapi import HTTPException

USER_FIELDS = [
    models.User.id,
    models.User.email,
    models.User.name,
    models.User.created_at,
]

USER_FIELDS_AND_PWD = USER_FIELDS.copy() + [models.User.password]


def create_user(body: schemas.User, db: Session) -> schemas.UserOut:
    body = body.model_dump()
    user = (
        db.execute(select(*USER_FIELDS).where(models.User.name == body["name"]))
        .scalars()
        .first()
    )

    if user:
        raise HTTPException(400, detail="Username is already in use")

    body["created_at"] = datetime.datetime.now(datetime.timezone.utc)
    user = models.User(**body)
    db.add(user)
    db.commit()
    db.refresh(user)
    return schemas.UserOut.model_validate(user)


def get_user(user_id: int, db: Session) -> Optional[schemas.UserOut]:
    user = (
        db.execute(select(*USER_FIELDS).where(models.User.id == user_id))
        .mappings()
        .first()
    )

    if user:
        return schemas.UserOut.model_validate(user)

    return None


def get_user_by_form(
    form: OAuth2PasswordRequestForm, db: Session
) -> Optional[schemas.UserOut]:
    user = db.execute(
        select(*USER_FIELDS_AND_PWD).where(models.User.name == form.username)
    ).first()

    if not user:
        return None

    if not verify_pwd(form.password, user.password):
        return None

    return user


# def get_user_by_email_form(
#     form: OAuth2PasswordRequestForm, db: Session
# ) -> Optional[schemas.UserOut]:
#     user = db.execute(
#         select(*USER_FIELDS_AND_PWD).where(models.User.email == form.username)
#     ).first()
    
#     if not user:
#         return None

#     code = send_code()


def update_user(user_id: int, body, db: Session) -> Optional[schemas.UserOut]:
    user = db.execute(
        update(models.User)
        .where(models.User.id == user_id)
        .returning(*USER_FIELDS)
        .values(**body.model_dump())
    ).first()

    if user:
        db.commit()
        return schemas.UserOut.model_validate(user)

    return None


def delete_user(user_id: int, db: Session) -> int:
    user_id = (
        db.execute(
            delete(models.User)
            .where(models.User.id == user_id)
            .returning(models.User.id)
        )
        .scalars()
        .first()
    )

    if user_id:
        db.commit()
        return user_id
    return None
