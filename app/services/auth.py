from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from ..database.database import Session
from ..database import models
from sqlalchemy import delete, select, update
from ..validation import schemas
from ..utils.hash import hash_pwd, verify_pwd
from ..utils.dependencies import create_refresh_token, create_token
from . import users

# тут будет логика routers/auth.py
# здесь будут хэшироваться пароли, токены; в users.py все должно приходить уже хешированное
# Что делает:
# Содержит логику безопасности:
#     Хеширование паролей
#     Проверка паролей
#     Генерация/валидация JWT-токенов
# Какие функции:
#     register_user – хеширует пароль и вызывает users.create_user
#     authenticate_user – проверяет email/пароль
#     create_access_token – генерирует JWT
#     verify_token – проверяет JWT


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


def logout():
    pass