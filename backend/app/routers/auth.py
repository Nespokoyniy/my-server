from fastapi import APIRouter, Depends

from backend.app.utils.dependencies import refresh_access_token
from ..validation import schemas
from ..database.database import get_db
from sqlalchemy.orm import Session
from ..utils.exc import db_exc_check
from ..services import auth
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/api", tags=["Auth", "API"])


@router.post("/register", status_code=201)
def register(body: schemas.User, db: Session = Depends(get_db)):
    db_exc_check(auth.register, {"body": body, "db": db})
    return {"message": "your account was registered"}


@router.post("/login", status_code=200, response_model=schemas.TokenResp)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return db_exc_check(auth.login, {"form": form, "db": db})

@router.post("/logout", status_code=204)
def logout(refresh_token: str, db: Session = Depends(get_db)):
    pass

@router.post("/refresh", status_code=200, response_model=schemas.TokenResp)
def refresh_token_pair(refresh_token: str, db: Session = Depends(get_db)):
    return refresh_access_token(refresh_token, db)

# @router.post("/login_with_email", status_code=200, response_model=schemas.TokenResp)
# def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
#     return db_exc_check(auth.login_with_email, {"form": form, "db": db})
