import pytest
from fastapi.testclient import TestClient
from app.main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def create_test_db():
    pass

# @pytest.fixture
# def get_test_db():
#     engine = create_engine(
#     f"postgresql+psycopg2://{ss.USERNAME}:{ss.PASSWORD}@{ss.IP_ADDRESS}:5432/{ss.DB_NAME}"
#     )
#     SessionLocal = sessionmaker(autoflush=False, bind=engine)
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()