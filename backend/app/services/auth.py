from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import delete
from ..database import models
from ..validation import schemas
from ..utils.hash import hash_pwd, verify_pwd
from ..utils.exc import db_exc_check
from ..utils.dependencies import create_token_pair
from . import users
import datetime
from jose import jwt
from ..config import settings as ss


def register(body: schemas.User, db: Session) -> bool:
    body.password = hash_pwd(body.password)
    user = users.create_user(body, db)
    return True


def login(form: OAuth2PasswordRequestForm, db: Session) -> schemas.TokenResp:
    user: schemas.UserOutByForm = db_exc_check(
        users.get_user_by_form, {"form": form, "db": db}
    )

    if user is None or not verify_pwd(form.password, user.password):
        raise HTTPException(400, detail="Invalid username or password")

    token_pair: schemas.TokenResp = create_token_pair(user.id)

    db.add(
        models.RefreshToken(
            token=token_pair.refresh_token,
            owner=user.id,
            expires_at=datetime.datetime.fromtimestamp(
                jwt.decode(
                    token_pair.refresh_token,
                    ss.REFRESH_SECRET_KEY,
                    algorithms=[ss.REFRESH_ALGORITHM],
                )["exp"]
            )
        )
    )

    return token_pair


def logout(refresh_token: str, db: Session) -> bool:
    db.execute(
        delete(models.RefreshToken).where(models.RefreshToken.token == refresh_token)
    )
    db.commit()
    return True


# def login_with_email(form: OAuth2PasswordRequestForm, db: Session) -> dict:
#     user = db_exc_check(users.get_user_by_email_form, {"form": form, "db": db})

#     if user is None:
#         raise HTTPException(404, detail="the email doesn't exist")

#     return {
#         "access_token": create_token(user.id),
#         "refresh_token": create_refresh_token(user.id),
#         "token_type": "bearer",
#     }
