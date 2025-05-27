from ..database import models
from sqlalchemy import delete, select, update
from ..validation import schemas
from ..utils.hash import hash_pwd
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

def register(body: schemas.User, db):
    body.password = hash_pwd(body.password)
    user = users.create_user(body, db)
    return user

def login(form):
    pass

def logout():
    pass