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
    SessionLocal = sessionmaker(autoflush=False, bind=engine)
    test_db = SessionLocal()
    return test_db


@pytest.fixture
def client(test_db):
    app.dependency_overrides[get_db] = lambda: test_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def register(client: TestClient):
    client.post(
        "/api/auth/register",
        json={
            "name": "example",
            "password": "example123",
            "email": "example@gmail.com",
        },
    )


@pytest.fixture
def token(client: TestClient, register):
    token = client.post(
        "/api/auth/login",
        data={"username": "example", "password": "example123"},
    )
    print(token)
    access_token = token.json()["access_token"]

    headers = {"Authorization": f"Bearer {access_token}"}
    return headers
