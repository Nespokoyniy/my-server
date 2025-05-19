from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from .models import Base

engine = create_engine("postgresql+psycopg2://postgres:roma123@192.168.0.115:5432/my-server-db")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    Base.metadata.create_all(engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
