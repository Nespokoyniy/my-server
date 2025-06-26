from fastapi import APIRouter, Depends
from ..validation import schemas
from ..database.database import Session, get_db
from ..utils.exc import db_exc_check
from ..services import users
from ..utils.dependencies import get_current_user

router = APIRouter(prefix="/api/profile", tags=["Profile", "API"])

@router.delete("/", status_code=204)
def delete_profile(
    user_id: int = Depends(get_current_user), db: Session = Depends(get_db)
):
    db_exc_check(users.delete_user, {"user_id": user_id, "db": db})
    return

@router.put("/", status_code=200)
def update_profile(
    body: schemas.User,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    updated_user = db_exc_check(
        users.update_user, {"user_id": user_id, "body": body, "db": db}
    )

    return updated_user

@router.get("/", status_code=200)
def get_profile(db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):
    user = users.get_user({"user_id": user_id, "db": db})

    return user