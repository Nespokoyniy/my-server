from fastapi import APIRouter, Depends
from ..validation import schemas
from ..database.database import Session, get_db
from ..utils.exc import db_exc_check
from ..services import auth
from fastapi.security import OAuth2PasswordRequestForm
from ..utils.dependencies import oauth2_scheme, verify_token

router = APIRouter(prefix="/auth", tags=["Prod", "Auth"])

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
    return {"message": "your account was registered"}

@router.post("/login")
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_exc_check(auth.login, (form, db))
    return {"message": "you are logged into your account"}

@router.post("/logout")
def logout(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    verify_token(token)
    auth.logout(token) #допиши