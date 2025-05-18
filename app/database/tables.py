from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Tasks(Base):
    __tablename__ = "tasks"

class RecurringTasks(Base):
    __tablename__ = "recur_tasks"

class Users(Base):
    __tablename__ = "users"