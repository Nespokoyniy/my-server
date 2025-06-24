from psycopg2 import IntegrityError
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException

def db_exc_check(func, args: dict):
    try:
        db = args["db"]
        resp = func(**args)
        if not resp:
            raise HTTPException(404, detail="data is invalid or doesn't exist")
        return resp
    except IntegrityError as e:
        db.rollback()
        print(e)
        raise HTTPException(400, detail="data integrity error")
    except SQLAlchemyError as e:
        db.rollback()
        print(e)
        raise HTTPException(500, detail="database operation failed")