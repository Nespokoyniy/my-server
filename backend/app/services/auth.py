from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from ..database.database import Session
from ..validation import schemas
from ..utils.hash import hash_pwd, verify_pwd
from ..utils.exc import db_exc_check
from ..utils.dependencies import create_refresh_token, create_token
from . import users


def register(body: schemas.User, db: Session):
    body.password = hash_pwd(body.password)
    user = users.create_user(body, db)
    return user


def login(form: OAuth2PasswordRequestForm, db: Session):
    user = db_exc_check(users.get_user_by_form, {"form": form, "db": db})

    if user is None or not verify_pwd(form.password, user["password"]):
        raise HTTPException(400, detail="Invalid username or password")
    return {
        "access_token": create_token(user["id"]),
        "refresh_token": create_refresh_token(user["id"]),
    }
