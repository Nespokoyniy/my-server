from fastapi.security import OAuth2PasswordRequestForm
import pytest
from fastapi.testclient import TestClient
from backend.app.database.database import get_db
from backend.app.main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from backend.app.config import settings as ss
from backend.app.services.auth import login, register
from backend.app.services.tasks import create_task
from backend.app.utils.dependencies import get_current_user
from backend.app.validation import schemas


@pytest.fixture
def test_db():
    engine = create_engine(ss.DB_URL)
    SessionLocal = sessionmaker(autoflush=False, bind=engine)
    test_db = SessionLocal()
    print("ONE")
    try:
        yield test_db
    finally:
        print("EIGHT")
        test_db.rollback()
        test_db.close()
        engine.dispose()


@pytest.fixture
def client(test_db):
    print("TWO")
    app.dependency_overrides[get_db] = lambda: test_db
    with TestClient(app) as test_client:
        yield test_client
    print("FIVE")
    app.dependency_overrides.clear()


@pytest.fixture
def token(test_db):
    try:
        register(
            schemas.User(
                name="example", email="example@gmail.com", password="example123"
            ),
            test_db,
        )
        print("THREE")

        token = login(
            OAuth2PasswordRequestForm(username="example", password="example123"),
            test_db,
        )

        access_token = token["access_token"]

        headers = {"Authorization": f"Bearer {access_token}"}
        print("FOUR")
        return headers
    except Exception:
        test_db.rollback()


@pytest.fixture
def create_tasks(token, test_db):
    print("SIX")
    user_id = get_current_user(token, test_db)
    for num in range(1, 4):
        create_task(
            schemas.TaskWithOwner(
                name=f"task {num}",
                description=f"desc {num}",
                priority=num,
                owner=user_id,
            ),
            test_db,
        )
    print("SEVEN")
