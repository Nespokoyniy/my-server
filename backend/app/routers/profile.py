from fastapi import APIRouter, Depends, Response
from ..validation import schemas
from ..database.database import get_db
from sqlalchemy.orm import Session
from ..utils.exc import db_exc_check
from ..services import users
from ..utils.dependencies import get_current_user

router = APIRouter(prefix="/api/profile", tags=["Profile", "API"])


@router.delete("/", status_code=204)
def delete_profile(
    user_id: int = Depends(get_current_user), db: Session = Depends(get_db)
):
    db_exc_check(users.delete_user, {"user_id": user_id, "db": db})
    return Response(status_code=204)


@router.put("/", status_code=200, response_model=schemas.UserOut)
def update_profile(
    body: schemas.User,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    updated_user = db_exc_check(
        users.update_user, {"user_id": user_id, "body": body, "db": db}
    )

    return updated_user


@router.get("/", status_code=200, response_model=schemas.UserOut)
def get_profile(
    db: Session = Depends(get_db), user_id: int = Depends(get_current_user)
):
    user = users.get_user(user_id, db)

    return user
