from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from ..database.database import Session
from ..validation import schemas
from ..utils.hash import hash_pwd, verify_pwd
from ..utils.dependencies import create_refresh_token, create_token
from . import users


def register(body: schemas.User, db: Session):
    body.password = hash_pwd(body.password)
    user = users.create_user(body, db)
    return user


def login(form: OAuth2PasswordRequestForm, db: Session):
    user = users.get_user_by_form(form, db)
    hashed_pwd = user["password"]
    if not verify_pwd(form.password, hashed_pwd) or user is None or not user:
        raise HTTPException(400, detail="Invalid username or password")
    
    return {
        "access_token": create_token(user["name"]),
        "refresh_token": create_refresh_token(user["name"]),
    }


def logout(token: str):
    del token