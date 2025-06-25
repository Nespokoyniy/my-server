from pydantic import BaseModel, EmailStr
from .enum import Weekdays

class Task(BaseModel):
    name: str
    description: str = None
    priority: int = 0
    
class RecurTask(Task):
    days: list[Weekdays]

class TaskWithOwner(Task):
    owner: int

class RecurTaskWithOwner(RecurTask):
    owner: int

class User(BaseModel):
    name: str
    email: EmailStr = None
    password: str

class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr = None
    
class Payload(BaseModel):
    sub: str
    exp: float
    iat: float