from fastapi.security import OAuth2PasswordRequestForm
from app.utils.hash import verify_pwd
from ..database.database import Session
from ..database import models
from sqlalchemy import delete, select, update

USER_FIELDS = [
    models.User.id,
    models.User.email,
    models.User.name,
    models.User.date_created,
]

USER_FIELDS_AND_PWD = USER_FIELDS.copy() + [models.User.password]


def create_user(body, db: Session):
    body = body.model_dump()
    user = models.User(**body)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user(user_id, db: Session):
    user = (
        db.execute(select(*USER_FIELDS).where(models.User.id == user_id)).mappings().first()
    )
    return user


def get_user_by_form(form: OAuth2PasswordRequestForm, db: Session):
    users = (
        db.execute(select(*USER_FIELDS_AND_PWD).where(models.User.name == form.username))
        .mappings()
        .all()
    )
    
    for user in users:
        if verify_pwd(form.password, user["password"]):
            return user
    return None


def update_user(user_id, body, db: Session):
    user = db.execute(
        update(models.User)
        .where(models.User.id == user_id)
        .returning(*USER_FIELDS)
        .values(**body.model_dump())
    ).first()

    db.commit()
    db.refresh(user)

    return user


def delete_user(user_id, db: Session):
    user = db.execute(
        delete(models.User).where(models.User.id == user_id).returning(models.User.id)
    ).mappings().first()
    
    db.commit()
    return user