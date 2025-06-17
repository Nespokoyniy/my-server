from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from ..config import settings as ss

engine = create_engine(
    f"postgresql+psycopg2://{ss.USERNAME}:{ss.PASSWORD}@{ss.IP_ADDRESS}:5432/{ss.DB_NAME}"
)

SessionLocal = sessionmaker(autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
