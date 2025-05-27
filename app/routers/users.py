from fastapi.routing import APIRouter
from fastapi import Depends, HTTPException
from sqlalchemy import delete, update, select
from app.database import models
from ..services import users
from ..database.database import Session, get_db
from ..utils.exc import db_exc_check
from ..validation import schemas

router = APIRouter(prefix="/api/users", tags=["Admin"])


@router.post("/", status_code=201)
def create_user(body: schemas.User, db: Session = Depends(get_db)):
    db_exc_check(users.create_user, (body, db))
    return {"message": "new user was created"}


@router.get("/{id}", status_code=200)
def get_user(id: int, db: Session = Depends(get_db)):
    user = users.get_user(id, db)

    if not user:
        raise HTTPException(404, detail=f"user doesn't exist")

    return user


@router.put("/{id}", status_code=200)
def update_user(body: schemas.User, id: int, db: Session = Depends(get_db)):
    db_exc_check(users.update_user, (id, body, db))

    return {"message": f"user {id} was updated"}


@router.delete("/{id}", status_code=204)
def delete_user(id: int, db: Session = Depends(get_db)):
    db_exc_check(users.delete_user, (id, db))
