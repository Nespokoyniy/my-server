from fastapi.routing import APIRouter

router = APIRouter()

@router.get("/auth_page")
def get_auth_page():
    pass