from ..database.database import Session
from typing import Any
from pydantic import BaseModel, EmailStr
from .enum import Weekdays

class Task(BaseModel):
    name: str
    description: str = ""
    priority: int = 0
    
class RecurTask(Task):
    days: list[Weekdays]

class User(BaseModel):
    name: str
    email: EmailStr = ""
    password: str
    
class ExcTuple(BaseModel):
    body: Any = None
    id: int = None
    name: str = None
    db: Any
    
class Payload(BaseModel):
    sub: str
    exp: int
    iat: int