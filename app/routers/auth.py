from fastapi.routing import APIRouter

router = APIRouter()

@router.post("/register")
def register():
    pass

@router.get("/login")
def login():
    pass