from fastapi import APIRouter, Depends, Response, HTTPException, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from ..database.database import get_db
from ..validation import schemas
from ..services import users
from ..utils.dependencies import get_current_user
from sqlalchemy import delete
from ..database import models
from datetime import datetime, timezone

router = APIRouter(prefix="/api/profile", tags=["Profile", "API"])
templates = Jinja2Templates(directory="frontend/templates")


@router.get("/partial", status_code=200)
def profile_partial(
    request: Request,
    db: Session = Depends(get_db), 
    # user_id: int = Depends(get_current_user)
):
    # user = users.get_user(user_id, db)
    user = schemas.UserOut(name="Roma", email="email@gmail.com", created_at=datetime.now(timezone.utc))
    return templates.TemplateResponse("partials/_profile_data.html", {
        "request": request,
        "user": user,
        "now": datetime.now(timezone.utc)
    })

@router.get("/edit-form", status_code=200)
def edit_profile_form(
    request: Request,
    db: Session = Depends(get_db), 
    user_id: int = Depends(get_current_user)
):
    user = users.get_user(user_id, db)
    return templates.TemplateResponse("partials/_profile_edit_form.html", {
        "request": request,
        "user": user
    })

# API эндпоинты остаются без изменений
@router.delete("/", status_code=204)
def delete_profile(user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    db.execute(delete(models.RefreshToken).where(models.RefreshToken.owner == user_id))
    db.commit()

    deleted = users.delete_user(user_id, db)

    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")

    return Response(status_code=204)

@router.patch("/", status_code=200, response_model=schemas.UserOut)
def update_profile(body: schemas.UserUpdate, db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):
    
    updated_user = users.update_user(user_id, body, db)
    if not updated_user:
        raise HTTPException(404, detail="User not found")
    return updated_user