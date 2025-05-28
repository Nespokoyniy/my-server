from fastapi.routing import APIRouter

router = APIRouter(tags=["Pages", "Prod"])

@router.get("/register") # ?
def get_register_page():
    pass

@router.get("/login") # ?
def get_login_page():
    pass

@router.get("/profile") # ?
def get_profile_page():
    pass

@router.get("/start") # ?
def get_start_page():
    pass

@router.get("/secret-page")
def get_secret_page():
    pass