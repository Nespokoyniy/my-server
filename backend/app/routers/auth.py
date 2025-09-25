# from fastapi import APIRouter, Depends, HTTPException, Response, Cookie
# from ..utils.dependencies import refresh_access_token, get_current_user
# from ..validation import schemas
# from ..services import auth
# from sqlalchemy.orm import Session
# from ..database.database import get_db
# from fastapi.security import OAuth2PasswordRequestForm

# router = APIRouter(prefix="/api", tags=["Auth", "API"])


# @router.post("/register", status_code=201)
# def register(body: schemas.User, db: Session = Depends(get_db)):
#     bool = auth.register(body, db)
#     if bool:
#         return {"message": "Successfully registered"}
#     raise HTTPException(500, detail="Registration failed")


# @router.post("/login", status_code=200, response_model=schemas.TokenResp)
# def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
#     return auth.login(form, db)


# @router.delete("/logout", status_code=204)
# def logout(
#     refresh_token: str = Cookie(None),
#     db: Session = Depends(get_db),
#     user_id: int = Depends(get_current_user),
# ):
#     if not refresh_token:
#         raise HTTPException(400, detail="Refresh token missing")

#     if auth.logout(refresh_token, db):
#         response = Response(status_code=204)
#         response.delete_cookie("access_token")
#         response.delete_cookie("refresh_token")
#         return response
#     raise HTTPException(500, detail="something went wrong in logout function")


# @router.post("/refresh", status_code=200, response_model=schemas.TokenResp)
# def refresh_token_pair(
#     refresh_token: str = Cookie(None),
#     db: Session = Depends(get_db)
# ):
#     if not refresh_token:
#         raise HTTPException(400, detail="Refresh token missing")
#     return refresh_access_token(refresh_token, db)

from fastapi import APIRouter, Depends, Form, HTTPException, Response, Cookie, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from ..utils.dependencies import refresh_access_token, get_current_user
from ..validation import schemas
from ..services import auth
from ..database.database import get_db
from typing import Optional

# Инициализируем Jinja2Templates
templates = Jinja2Templates(directory="frontend/templates")

router = APIRouter(tags=["Auth", "API"])

@router.post("/register", status_code=200)
def register_user(request: Request, body: schemas.User, db: Session = Depends(get_db)):
    """
    Эндпоинт для обработки данных формы регистрации, используемый HTMX.
    """
    # Проверка, что пароли совпадают, если в форме есть confirm_password
    # Эта логика должна быть в сервисной части или валидации, но пока добавим сюда
    if body.password != request.get("confirm_password"):
        raise HTTPException(400, detail="Passwords do not match")
    
    # Обработка регистрации
    success = auth.register(body, db)
    if not success:
        raise HTTPException(500, detail="Registration failed")
    
    # При успешной регистрации возвращаем фрагмент с сообщением
    return templates.TemplateResponse("auth/partials/registration_success.html", {"request": request})


@router.delete("/api/logout", status_code=204)
def logout_user(
    refresh_token: str = Cookie(None),
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    """
    Эндпоинт для выхода.
    """
    if not refresh_token:
        raise HTTPException(400, detail="Refresh token missing")

    if auth.logout(refresh_token, db):
        response = Response(status_code=204)
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return response
    raise HTTPException(500, detail="something went wrong in logout function")


@router.post("/api/refresh", status_code=200, response_model=schemas.TokenResp)
def refresh_token_pair(
    refresh_token: str = Cookie(None),
    db: Session = Depends(get_db)
):
    """
    Эндпоинт для обновления токенов.
    """
    if not refresh_token:
        raise HTTPException(400, detail="Refresh token missing")
    return refresh_access_token(refresh_token, db)

@router.post("/api/login", response_class=HTMLResponse)
def login_user(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
    response: Response = Response()
):
    """
    Эндпоинт для входа, адаптированный для HTMX.
    Возвращает редирект или HTML с ошибкой.
    """
    form = OAuth2PasswordRequestForm(username=username, password=password)
    try:
        # Ваш сервис `auth.login` должен возвращать `RedirectResponse` или `TokenResp`
        token_pair = auth.login(form=form, db=db, response=response)
        
        # Если login успешный, то response будет содержать куки и HTMX перенаправит на dashboard
        # hx-redirect должен быть установлен в заголовках ответа
        response.headers["HX-Redirect"] = "/dashboard"
        return response
    except HTTPException as e:
        if e.status_code == 400:
            # Возвращаем HTML-фрагмент с сообщением об ошибке
            error_message = "Неверное имя пользователя или пароль."
            return templates.TemplateResponse(
                "partials/error_message.html", {"request": request, "error": error_message}
            )
        raise e