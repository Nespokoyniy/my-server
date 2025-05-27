from fastapi import APIRouter

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
def register():
    pass

@router.post("/login")
def login():
    pass

@router.post("/logout")
def logout():
    pass