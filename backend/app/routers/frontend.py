from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from ..utils.dependencies import get_current_user

router = APIRouter(tags=["Frontend", "For Users"])
templates = Jinja2Templates("../frontend/templates")

@router.get("/", status_code=200, response_model=HTMLResponse)
def dashboard(request: Request, user_id: int = Depends(get_current_user)):
    pass