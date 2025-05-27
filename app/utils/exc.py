from psycopg2 import IntegrityError
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException

def db_exc_check(func, args: tuple):
    try:
        db = args[-1]
        resp = func(*args)
        return resp
    except IntegrityError:
        db.rollback()
        raise HTTPException(400, detail="data integrity error")
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(500, detail="database operation failed")