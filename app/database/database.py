from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from .models import Base
from .config import settings as ss

engine = create_engine(
    f"postgresql+psycopg2://{ss.USERNAME}:{ss.PASSWORD}@{ss.IP_ADDRESS}:{ss.PORT}/{ss.DB_NAME}"
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    Base.metadata.create_all(engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
