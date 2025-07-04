from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict
from .enum import Weekdays
from typing import Optional


class MainModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class Task(MainModel):
    name: str
    description: Optional[str] = None
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


class User(MainModel):
    name: str
    email: Optional[EmailStr] = None
    password: str


class UserOut(MainModel):
    name: str
    email: Optional[EmailStr] = None
    date_created: datetime


class Payload(MainModel):
    sub: str
    exp: float
    iat: float


class TokenResp(MainModel):
    access_token: str
    refresh_token: str
    token_type: str
