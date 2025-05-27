from ..config import settings as ss
from jose import jwt
from datetime import datetime, timedelta, timezone

SECRET_KEY = ss.SECRET_KEY
TOKEN_EXPIRE_MINUTES = ss.TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_MINUTES = ss.REFRESH_TOKEN_EXPIRE_MINUTES
ALGORITHM = ss.ALGORITHM
REFRESH_ALGORITHM = ss.REFRESH_ALGORITHM
REFRESH_SECRET_KEY = ss.REFRESH_SECRET_KEY

def create_token(subject: str, expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.now(timezone.utc) + expires_delta
    else:
        expires_delta = datetime.now(timezone.utc) + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    
    if not subject:
        raise ValueError("Subject must be non-empty string")
    
    to_encode = {"sub": str(subject), "exp": expires_delta}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return encoded_jwt
    
def create_refresh_token(subject: str, expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.now(timezone.utc) + expires_delta
    else:
        expires_delta = datetime.now(timezone.utc) + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
        
    if not subject:
        raise ValueError("Subject must be non-empty string")    
        
    to_encode = {"sub": str(subject), "exp": expires_delta}
    encoded_jwt = jwt.encode(to_encode, REFRESH_SECRET_KEY, ALGORITHM)
    return encoded_jwt
    

def decode_token():
    pass

def verify_token():
    pass