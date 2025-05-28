from psycopg2 import IntegrityError
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from ..validation import schemas

def db_exc_check(func, args: schemas.ExcTuple):
    try:
        db = args[-1]
        resp = func(*args)
        return resp
    except IntegrityError:
        db.rollback()
        raise HTTPException(400, detail="data integrity error")
    