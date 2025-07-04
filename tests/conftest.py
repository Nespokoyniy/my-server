import pytest
from fastapi.testclient import TestClient
from backend.app.database.database import get_db
from backend.app.main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.app.config import settings as ss
from backend.app.main import app


@pytest.fixture
def test_db():
    engine = create_engine(ss.DB_URL)
    connection = engine.connect()
    transaction = connection.begin()
    SessionLocal = sessionmaker(autoflush=False, bind=connection)
    test_db = SessionLocal()
    
    yield test_db
    
    test_db.close()
    transaction.rollback()
    connection.close()
    


@pytest.fixture
def client(test_db):
    app.dependency_overrides[get_db] = lambda: test_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def token(client: TestClient):
    resp = client.post(
        "/api/auth/register",
        json={
            "name": "example",
            "email": "example@gmail.com",
            "password": "example123",
        },
    )

    token = client.post(
        "/api/auth/login",
        data={"username": "example", "password": "example123"},
    )

    access_token = token.json()["access_token"]

    headers = {"Authorization": f"Bearer {access_token}"}
    return headers