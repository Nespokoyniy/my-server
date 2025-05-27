from fastapi import APIRouter, Depends
from ..validation import schemas
from ..database.database import Session, get_db
from ..utils.exc import db_exc_check
from ..services import auth
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/auth")

# тут будет пользовательский интерфейс
# Что делает:
# Обрабатывает запросы на аутентификацию (вход/регистрацию).
# Какие эндпоинты:
#     POST /auth/register – регистрация
#     POST /auth/login – вход
#     POST /auth/logout – выход (опционально)
# Что вызывает:
#     Методы из services/auth.py.


@router.post("/register")
def register(body: schemas.User, db: Session = Depends(get_db)):
    db_exc_check(auth.register, (body, db))
    return {"message": "you was registered successfully"}

@router.post("/login")
def login(form: OAuth2PasswordRequestForm = Depends()):
    pass

@router.post("/logout")
def logout():
    pass