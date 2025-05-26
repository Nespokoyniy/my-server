from fastapi import APIRouter

router = APIRouter("/auth")

@router.post("/register")
def register():
    pass

@router.post("/login")
def login():
    pass

@router.post("/logout")
def logout():
    pass