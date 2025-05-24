from fastapi.routing import APIRouter
from fastapi import Depends, HTTPException
from sqlalchemy import delete, update, select
from app.database import models
from security.hash import hash_pwd
from ..validation import schemas
from ..database.database import Session, get_db

router = APIRouter(prefix="/api/auth")


@router.post("/", status_code=201)
def create_user(body: schemas.User, db: Session = Depends(get_db)):
    body = body.model_dump()
    body["password"] = hash_pwd(body["password"])
    user = models.User(**body)
    db.add(user)
    db.commit()
    return {"message": "user was created successfully"}


@router.get("/{id}", status_code=200)
def get_user(id: int, db: Session = Depends(get_db)):
    user = (
        db.execute(
            select(
                models.User.id,
                models.User.email,
                models.User.name,
                models.User.date_created,
                models.User.password,
            )
        )
        .mappings()
        .first()
    )

    if not user:
        raise HTTPException(404, detail=f"user doesn't exist")

    return user


@router.put("/{id}", status_code=200)
def update_user(body: schemas.User, id: int, db: Session = Depends(get_db)):
    user = db.execute(
        update(models.User)
        .where(models.User.id == id)
        .returning(
            models.User.id,
            models.User.email,
            models.User.name,
            models.User.date_created,
            models.User.password,
        )
        .values(**body.model_dump())
    ).first()

    if not user:
        raise HTTPException(404, detail="user doesn't exist")

    return user


@router.delete("/{id}", status_code=204)
def delete_user(id: int, db: Session = Depends(get_db)):
    user = db.execute(
        delete(models.User).where(models.User.id == id).returning(models.User.id)
    ).first()

    if not user:
        raise HTTPException(404, detail="user doesn't exist")

    return user
