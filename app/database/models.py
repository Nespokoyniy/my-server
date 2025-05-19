import datetime
from sqlalchemy import Column, DateTime, Integer, String, TIMESTAMP
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    date_created = Column(
        DateTime(timezone=True), default=datetime.datetime.now(datetime.timezone.utc)
    )


class RecurringTask(Base):
    __tablename__ = "recur_tasks"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    date_created = Column(
        DateTime(timezone=True), default=datetime.datetime.now(datetime.timezone.utc)
    )


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    password = Column(Integer, nullable=False)
    date_created = Column(
        DateTime(timezone=True), default=datetime.datetime.now(datetime.timezone.utc)
    )
