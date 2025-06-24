from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError
from ..config import settings as ss
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from ..validation.schemas import Payload
from fastapi import Depends, HTTPException

SECRET_KEY = ss.SECRET_KEY
TOKEN_EXPIRE_MINUTES = ss.TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_MINUTES = ss.REFRESH_TOKEN_EXPIRE_MINUTES
ALGORITHM = ss.ALGORITHM
REFRESH_ALGORITHM = ss.REFRESH_ALGORITHM
REFRESH_SECRET_KEY = ss.REFRESH_SECRET_KEY
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login", scheme_name="JWT")


def create_token(subject_id: int, expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.now(timezone.utc) + expires_delta
    else:
        expires_delta = datetime.now(timezone.utc) + timedelta(
            minutes=TOKEN_EXPIRE_MINUTES
        )

    if not subject_id:
        raise ValueError("Subject must be non-empty string")

    to_encode = {
        "sub": str(subject_id),
        "exp": expires_delta.timestamp(),
        "iat": datetime.now(timezone.utc).timestamp(),
    }
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return encoded_jwt


def create_refresh_token(subject_id: int, expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.now(timezone.utc) + expires_delta
    else:
        expires_delta = datetime.now(timezone.utc) + timedelta(
            minutes=REFRESH_TOKEN_EXPIRE_MINUTES
        )

    if not subject_id:
        raise ValueError("Subject must be non-empty string")

    to_encode = {
        "sub": str(subject_id),
        "exp": expires_delta.timestamp(),
        "iat": datetime.now(timezone.utc).timestamp(),
    }
    encoded_jwt = jwt.encode(to_encode, REFRESH_SECRET_KEY, REFRESH_ALGORITHM)
    return encoded_jwt


def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, key=SECRET_KEY, algorithms=ALGORITHM)
        token_data = Payload(**payload)
        user_id = int(token_data.sub)

        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                401, detail="Token expired", headers={"WWW-Authenticate": "Bearer"}
            )

    except (JWTError, ValidationError):
        raise HTTPException(403, detail="Could not validate credentials")

    return user_id


def get_current_user(token: str = Depends(oauth2_scheme)):
    user_id = verify_token(token)
    return user_id
