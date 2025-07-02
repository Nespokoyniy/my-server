from datetime import datetime
from pydantic import BaseModel, EmailStr
from .enum import Weekdays

class Task(BaseModel):
    name: str
    description: str = None
    priority: int = 0
    
class TaskOut(Task):
    user_task_id: int
    is_completed: bool
    date_created: datetime
    

class RecurTask(Task):
    days: list[Weekdays]
    
class RecurTaskOut(RecurTask):
    user_task_id: int
    is_completed: bool
    date_created: datetime
    
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
    date_created: datetime
    
class Payload(BaseModel):
    sub: str
    exp: float
    iat: float
    
class TokenResp(BaseModel):
    access_token: str
    refresh_token: str