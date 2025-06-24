import pytest
from fastapi.testclient import TestClient
from backend.app.main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.app.config import settings as ss

engine = create_engine(ss.TEST_DB_URL)
SessionLocal = sessionmaker(autoflush=False, bind=engine)

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def create_test_db():
    pass


@pytest.fixture
def get_test_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()