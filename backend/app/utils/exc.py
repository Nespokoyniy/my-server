from typing import Any, Callable
from functools import wraps
from psycopg2 import IntegrityError
from sqlalchemy import HasSuffixes
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
import logging
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


def db_exc_check(func: Callable) -> Any:
    @wraps(func)
    def wrapper(*args, **kwargs):
        db = None
        for arg in args:
            if isinstance(arg, Session):
                db = arg
                break     
            elif hasattr(arg, "rollback"):
                db = arg

        if not db:
            for value in kwargs.values():
                if isinstance(value, Session):
                    db = value
                    break
                elif hasattr(value, "rollback"):
                    db = value
                    break
                
        try:
            return func(*args, **kwargs)
        except IntegrityError as e:
            if db:
                db.rollback()
            logger.error("Database integrity error", exc_info=e)
            raise HTTPException(400, detail="Data integrity error")
        except SQLAlchemyError as e:
            if db:
                db.rollback()
            logger.error("Database operation error", exc_info=e)
            raise HTTPException(500, detail="Database operation failed")
        except ValueError as e:
            if db:
                db.rollback()
            logger.error("Value error", exc_info=e)
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            if db:
                db.rollback()
            logger.error("Unexpected error", exc_info=e)
            raise HTTPException(500, detail="Internal server error")

    return wrapper
