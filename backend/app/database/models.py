import datetime
from sqlalchemy import Column, DateTime, Integer, String, ARRAY, Boolean
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, unique=True)
    user_task_id = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    date_created = Column(
        DateTime(timezone=True), default=datetime.datetime.now(datetime.timezone.utc)
    )
    owner = Column(Integer, nullable=False)
    is_completed = Column(Boolean, default=False)
    priority = Column(Integer, default=0)


class RecurringTask(Base):
    __tablename__ = "recur_tasks"
    id = Column(Integer, primary_key=True, unique=True)
    user_task_id = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    date_created = Column(
        DateTime(timezone=True), default=datetime.datetime.now(datetime.timezone.utc)
    )
    owner = Column(Integer, nullable=False)
    is_completed = Column(Boolean, default=False)
    priority = Column(Integer, default=0)
    days = Column(ARRAY(String), nullable=False)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String, unique=False, nullable=False)
    email = Column(String, nullable=True)
    password = Column(String, nullable=False)
    date_created = Column(
        DateTime(timezone=True), default=datetime.datetime.now(datetime.timezone.utc)
    )