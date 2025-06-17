from fastapi import APIRouter, Depends
from ..validation import schemas
from ..database.database import Session, get_db
from ..utils.exc import db_exc_check
from ..services import auth, users
from fastapi.security import OAuth2PasswordRequestForm
from ..utils.dependencies import oauth2_scheme, verify_token

router = APIRouter(prefix="/auth", tags=["Prod", "Auth"])

@router.post("/register", status_code=201)
def register(body: schemas.User, db: Session = Depends(get_db)):
    db_exc_check(auth.register,  {"body": body, "db": db})
    return {"message": "your account was registered"}

@router.post("/login", status_code=201)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return db_exc_check(auth.login, {"form": form, "db": db})

@router.post("/delete", status_code=204)
def delete_account(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user_id = verify_token(token)
    db_exc_check(users.delete_user, {"user_id": user_id, "db": db})