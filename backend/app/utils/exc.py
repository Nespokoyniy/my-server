from typing import Any, Callable
from psycopg2 import IntegrityError
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException


def db_exc_check(func: Callable, args: dict) -> Any:
    try:
        db = args["db"]
        resp = func(**args)
        return resp

    except IntegrityError as e:
        db.rollback()
        print(e)
        raise HTTPException(400, detail="data integrity error")

    except SQLAlchemyError as e:
        db.rollback()
        print(e)
        raise HTTPException(500, detail="database operation failed")

    except ValueError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
