from fastapi.routing import APIRouter
from fastapi import Depends
from ..services import users
from ..database.database import Session, get_db
from ..utils.exc import db_exc_check
from ..validation import schemas
from ..utils.dependencies import get_current_user

router = APIRouter(prefix="/api/users", tags=["Users", "API", "Admin"])


@router.get("/", status_code=200)
def get_user(db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):
    user = users.get_user({"user_id": user_id, "db": db})

    return user


@router.put("/", status_code=200)
def update_user(
    body: schemas.User,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    updated_user = db_exc_check(
        users.update_user, {"user_id": user_id, "body": body, "db": db}
    )

    return updated_user
