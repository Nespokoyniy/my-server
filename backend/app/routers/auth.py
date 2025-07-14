from fastapi import APIRouter, Depends, HTTPException
from ..utils.dependencies import refresh_access_token
from ..validation import schemas
from ..database.database import get_db
from sqlalchemy.orm import Session
from ..utils.exc import db_exc_check
from ..services import auth
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/api", tags=["Auth", "API"])


@router.post("/register", status_code=201)
def register(body: schemas.User, db: Session = Depends(get_db)):
    bool = db_exc_check(auth.register, {"body": body, "db": db})
    if bool:
        return {"message": "Successfully registered"}
    raise HTTPException(500, detail="something went wrong in register function")


@router.post("/login", status_code=200, response_model=schemas.TokenResp)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return db_exc_check(auth.login, {"form": form, "db": db})


@router.post("/logout", status_code=204)
def logout(refresh_token: str, db: Session = Depends(get_db)):
    bool = db_exc_check(auth.logout, {"refresh_token": refresh_token, "db": db})
    
    if bool:
        return {"message": "Successfully logged out"}
    raise HTTPException(500, detail="something went wrong in logout function")


@router.post("/refresh", status_code=200, response_model=schemas.TokenResp)
def refresh_token_pair(refresh_token: str, db: Session = Depends(get_db)):
    return refresh_access_token(refresh_token, db)


# @router.post("/login_with_email", status_code=200, response_model=schemas.TokenResp)
# def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
#     return db_exc_check(auth.login_with_email, {"form": form, "db": db})
